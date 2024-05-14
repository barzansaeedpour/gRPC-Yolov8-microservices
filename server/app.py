import grpc
import cv2
import time
from concurrent import futures
import camera_pb2
import camera_pb2_grpc
import GetServiceClaims_pb2
import GetServiceClaims_pb2_grpc
from datetime import datetime
import shutil
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
base_dir = os.getenv("base_dir_server")
server_grpc_channel_address = os.getenv("server_grpc_channel_address")



def get_new_name():
    # Get the current date and time
    current_datetime = datetime.now()
    # Format the datetime as desired (e.g., YYYYMMDD-HHMMSS)
    formatted_datetime = current_datetime.strftime("%Y%m%d-%H%M%S")
    # Create a unique filename
    filename = f"my_file_{formatted_datetime}"
    # print(f"Unique filename: {filename}")
    return filename

class CameraServicer(camera_pb2_grpc.CameraServicer):
    def StreamCamera(self, request_iterator, context):
        # Initialize camera (replace with your actual camera setup)
        video_path = f'{base_dir}/files/video_test.mp4'
        saved_images = f'{base_dir}/saved_images/'
        try:
            shutil.rmtree(saved_images)
        except:
            pass
        os.makedirs(saved_images, exist_ok=True)
        # print(video_path)
        
        # cap = cv2.VideoCapture(0)
        cap = cv2.VideoCapture(video_path)
        
        try:
            while True:
                ret, frame = cap.read()
                # print(ret)
                
                # new_name = get_new_name()
                # cv2.imwrite(f"{saved_images}{new_name}.png", frame)
                
                if not ret:
                    break

                # Convert frame to bytes
                # print(frame)
                frame_bytes = cv2.imencode('.jpg', frame)[1].tobytes()

                # Yield the frame to the client
                yield camera_pb2.CameraFrame(frame=frame_bytes)

                # Simulate camera frame rate (adjust as needed)
                time.sleep(0.1)
        finally:
            cap.release()
            

class GetServiceClaims(GetServiceClaims_pb2_grpc.GetClaimsServicer):
    def GetClaimsList(self, request, context):
        
        dotenv_path = find_dotenv()
        load_dotenv(dotenv_path)
        base_dir = os.getenv("base_dir_camera_webapp")
        db_engine = create_engine(f'sqlite:///{base_dir}/test.db')
        
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

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # camera_pb2_grpc.add_CameraServicer_to_server(CameraServicer(), server)
    GetServiceClaims_pb2_grpc.add_GetClaimsServicer_to_server(GetServiceClaims(), server)
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
