import grpc
import cv2
import time
from concurrent import futures
from stream_camera_from_back_service import stream_camera_from_back_service
# import camera_pb2
# import camera_pb2_grpc
# import Camera_pb2
# import Camera_pb2_grpc
# import PlateDetection_pb2
# import PlateDetection_pb2_grpc
import ReadPlate_pb2
import ReadPlate_pb2_grpc
import GetServiceClaims_pb2
import GetServiceClaims_pb2_grpc
import Camera_pb2
import Camera_pb2_grpc
from datetime import datetime
import shutil
import os
import numpy as np
import pandas as pd
import json
from sqlalchemy import create_engine
from dotenv import find_dotenv, load_dotenv
from my_yolo_v8.yolov8 import plate_detection
from my_yolo_v8.rabbitmq.publisher import publish


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
base_dir = os.getenv("base_dir_plate_detection")
server_grpc_channel_address = os.getenv("server_grpc_channel_address")
postgresql_user = os.getenv('postgresql_user')
postgresql_password = os.getenv("postgresql_password")
client_grpc_channel_address = os.getenv("client_grpc_channel_address")
save_dir = f'{base_dir}/saved_images/'
# plate_detection_output_path = f"{base_dir}/my_yolo_v8/outputs/"
plate_detection_output_path = f"{base_dir}/detected_plates/"

try:
    shutil.rmtree(save_dir)
except:
    pass
os.makedirs(save_dir, exist_ok=True)
try:
    shutil.rmtree(plate_detection_output_path)
except:
    pass
os.makedirs(plate_detection_output_path, exist_ok=True)


def get_new_name():
    # Get the current date and time
    current_datetime = datetime.now()
    # Format the datetime as desired (e.g., YYYYMMDD-HHMMSS)
    formatted_datetime = current_datetime.strftime("%Y%m%d-%H%M%S")
    # Create a unique filename
    filename = f"my_file_{formatted_datetime}"
    # print(f"Unique filename: {filename}")
    return filename

# class CameraServicer(camera_pb2_grpc.CameraServicer):
#     def StreamCamera(self, request_iterator, context):
#         # Initialize camera (replace with your actual camera setup)
#         video_path = f'{base_dir}/files/video_test.mp4'
#         saved_images = f'{base_dir}/saved_images/'
#         try:
#             shutil.rmtree(saved_images)
#         except:
#             pass
#         os.makedirs(saved_images, exist_ok=True)
        
#         # print(video_path)
        
#         # cap = cv2.VideoCapture(0)
#         # cap = cv2.VideoCapture(video_path)
        
#         # try:
#         #     while True:
#         #         ret, frame = cap.read()
#         #         # print(ret)
                
#         #         # new_name = get_new_name()
#         #         # cv2.imwrite(f"{saved_images}{new_name}.png", frame)
                
#         #         if not ret:
#         #             break

#         #         # Convert frame to bytes
#         #         # print(frame)
#         #         frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()

#         #         # Yield the frame to the client
#         #         yield camera_pb2.CameraFrame(frame=frame_bytes)

#         #         # Simulate camera frame rate (adjust as needed)
#         #         time.sleep(0.1)
#         # finally:
#         #     cap.release()
            

class GetServiceClaims(GetServiceClaims_pb2_grpc.GetClaimsServicer):
    def GetClaimsList(self, request, context):
        
        dotenv_path = find_dotenv()
        load_dotenv(dotenv_path)
        base_dir = os.getenv("base_dir_camera_webapp")
        # db_engine = create_engine(f'sqlite:///{base_dir}/test.db')
        db_engine = create_engine(f'postgresql://{postgresql_user}:{postgresql_password}@localhost')
        
        table_name = 'claim' 
        df = pd.read_sql_table(table_name, db_engine)
        claims_from_db = list(df.title)
        print(claims_from_db)

        claims = []
        for claim in claims_from_db:
            # claims.append(claims_pb2.Claim(
            #     title=claim,
            # ))
            claims.append(claim)
        return GetServiceClaims_pb2.GetClaimListReply(items=claims)

class ReadPlate(ReadPlate_pb2_grpc.ReadPlateServicer):
    def ReadPlates(self, request, context):
        detected_plates = {}
        with grpc.insecure_channel(client_grpc_channel_address) as channel:
            stub = Camera_pb2_grpc.CameraStub(channel)
            try:
                for response in stub.StreamImages(Camera_pb2.ImageStreamRequest(connection_string="rtsp://192.168.100.7/onvif1",
                                                                                FramePerSecond=2,
                                                                                Password="admin",
                                                                                UserName="admin"
                                                                                )):
                    base64_frame = response.ImageData
                    nparr = np.frombuffer(base64_frame, np.uint8)
                    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    # new_name = get_new_name()
                    # b = cv2.imwrite(f"{save_dir}{new_name}.png", frame)
                    detected_plate = plate_detection(frame, save_dir=plate_detection_output_path)
                    if detected_plate:
                        if detected_plate in detected_plates.keys():
                            detected_plates[detected_plate] +=1
                            if detected_plates[detected_plate] > 5:
                                publish(plate= detected_plate)
                                print(200*'*')
                        else:
                            detected_plates[detected_plate] = 1
                        with open(f"{plate_detection_output_path}detection_counter.json", "w") as file:
                                # file.write(f"{str(detected_plates)}\n")
                                json.dump(detected_plates, file)
                    new_name = get_new_name()
                    # print(new_name)
                    b = cv2.imwrite(f"{save_dir}{new_name}.png", frame)

            except KeyboardInterrupt:
                pass
            finally:
                cv2.destroyAllWindows()
        # x = stream_camera_from_back_service()
        # print(x)
        # for i in range(10):
        #     time.sleep(1)
        #     yield ReadPlate_pb2.ReadPlateReply(plate=f'11dal2225{i}', image_path='C://temp')

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # PlateDetection_pb2_grpc.add_PlateDetectionServicer_to_server(CameraServicer(), server)
    # GetServiceClaims_pb2_grpc.add_GetClaimsServicer_to_server(GetServiceClaims(), server)
    ReadPlate_pb2_grpc.add_ReadPlateServicer_to_server(ReadPlate(), server)
    # server.add_insecure_port('[::]:50051')
    server.add_insecure_port(server_grpc_channel_address)
    # server.add_insecure_port('127.0.0.1:50051')
    server.start()
    # print("Server started on port 50051")
    print("Server started on port 81")
    try:
        while True:
            time.sleep(60 * 60 * 24)  # Keep server running
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
