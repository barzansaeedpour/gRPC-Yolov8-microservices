import shutil
import grpc
import cv2
import Camera_pb2
import Camera_pb2_grpc
import ReadPlate_pb2
import ReadPlate_pb2_grpc
import numpy as np
from datetime import datetime
import os
from dotenv import find_dotenv, load_dotenv
import json
from my_yolo_v8.yolov8 import plate_detection
from my_yolo_v8.rabbitmq.publisher import publish
import io, base64
from PIL import Image
###################################################
# from flask import Flask, request, jsonify
# from flask_socketio import SocketIO, emit
# from flask_cors import CORS
######################################


dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
base_dir = os.getenv("base_dir_client")
client_grpc_channel_address = os.getenv("client_grpc_channel_address")

save_dir = f'{base_dir}/saved_images/'
plate_detection_output_path = f"{base_dir}/my_yolo_v8/outputs/"


try:
    shutil.rmtree(save_dir)
except:
    pass
os.makedirs(save_dir, exist_ok=True)


def get_new_name():
    # Get the current date and time
    current_datetime = datetime.now()
    # Format the datetime as desired (e.g., YYYYMMDD-HHMMSS)
    formatted_datetime = current_datetime.strftime("%Y%m%d-%H%M%S")
    # Create a unique filename
    filename = f"my_file_{formatted_datetime}"
    # print(f"Unique filename: {filename}")
    return filename


def stream_camera_from_back_service():
    #     {
    #     "connection_string": "rtsp://192.168.100.7/onvif1",
    #     "FramePerSecond": 2,
    #     "Password": "admin",
    #     "UserName": "admin"
    # }
    # detected_plates = {}
    with grpc.insecure_channel(client_grpc_channel_address) as channel:
        stub = Camera_pb2_grpc.CameraStub(channel)
        # response = stub.StreamCamera(camera_pb2.CameraFrame())
        # print(response)
        try:
            for response in stub.StreamImages(Camera_pb2.ImageStreamRequest(connection_string="rtsp://192.168.100.7/onvif1",
                                                                            FramePerSecond=2,
                                                                            Password="admin",
                                                                            UserName="admin"
                                                                            )):
                base64_frame = response.ImageData
                nparr = np.frombuffer(base64_frame, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                # img = Image.open(io.BytesIO(base64.decodebytes(bytes(base64_frame, "utf-8"))))
                # frame = base64.b64decode(base64_frame)
                new_name = get_new_name()
                # print(new_name)
                b = cv2.imwrite(f"{save_dir}{new_name}.png", frame)
                
                # # Process the received frame (e.g., display it)
                # # print("Success")
                # frame = response.frame
                # nparr = np.frombuffer(frame, np.uint8)
                # frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                # detected_plate = plate_detection(frame)
                # if detected_plate:
                #     if detected_plate in detected_plates.keys():
                #         detected_plates[detected_plate] +=1
                #         with open(f"{plate_detection_output_path}detection_counter.json", "w") as file:
                #             # file.write(f"{str(detected_plates)}\n")
                #             json.dump(detected_plates, file)
                #         if detected_plates[detected_plate] > 5:
                #             publish(plate= detected_plate)
                #             print(200*'*')

                #     else:
                #         detected_plates[detected_plate] = 1
                # new_name = get_new_name()
                # # print(new_name)
                # b = cv2.imwrite(f"{save_dir}{new_name}.png", frame)

        except KeyboardInterrupt:
            pass
        finally:
            cv2.destroyAllWindows()
            
def ReadPlate():
    with grpc.insecure_channel(client_grpc_channel_address) as channel:
        stub = ReadPlate_pb2_grpc.ReadPlateStub(channel)
        try:
            for response in stub.ReadPlates(ReadPlate_pb2.ReadPlateRequest(guid='shdjfsd-sdf-as-dfasdf-asdf')):
                pass
        except KeyboardInterrupt:
            pass
        finally:
            cv2.destroyAllWindows()


# def stream_camera():
#     detected_plates = {}
#     with grpc.insecure_channel(client_grpc_channel_address) as channel:
#         stub = camera_pb2_grpc.CameraStub(channel)
#         # response = stub.StreamCamera(camera_pb2.CameraFrame())
#         # print(response)
#         try:
#             for response in stub.StreamCamera(camera_pb2.CameraFrame()):
#                 # Process the received frame (e.g., display it)
#                 # print("Success")
#                 frame = response.frame
#                 nparr = np.frombuffer(frame, np.uint8)
#                 frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
#                 detected_plate = plate_detection(frame)
#                 if detected_plate:
#                     if detected_plate in detected_plates.keys():
#                         detected_plates[detected_plate] +=1
#                         with open(f"{plate_detection_output_path}detection_counter.json", "w") as file:
#                             # file.write(f"{str(detected_plates)}\n")
#                             json.dump(detected_plates, file)
#                         if detected_plates[detected_plate] > 5:
#                             publish(plate= detected_plate)
#                             print(200*'*')

#                     else:
#                         detected_plates[detected_plate] = 1
#                 new_name = get_new_name()
#                 # print(new_name)
#                 b = cv2.imwrite(f"{save_dir}{new_name}.png", frame)
#         except KeyboardInterrupt:
#             pass
#         finally:
#             cv2.destroyAllWindows()
if __name__ == '__main__':
    # stream_camera()
    # stream_camera_from_back_service()
    ReadPlate()
