import grpc
import cv2
import camera_pb2
import camera_pb2_grpc
import numpy as np
from datetime import datetime
import os
from dotenv import find_dotenv, load_dotenv
import json
from my_yolo_v8.yolov8 import plate_detection
from my_yolo_v8.rabbitmq.publisher import publish
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


import shutil
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




def stream_camera():
    detected_plates = {}
    with grpc.insecure_channel(client_grpc_channel_address) as channel:
        stub = camera_pb2_grpc.CameraStub(channel)
        # response = stub.StreamCamera(camera_pb2.CameraFrame())
        # print(response)
        try:
            for response in stub.StreamCamera(camera_pb2.CameraFrame()):
                # Process the received frame (e.g., display it)
                # print("Success")
                frame = response.frame
                nparr = np.frombuffer(frame, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                detected_plate = plate_detection(frame)
                if detected_plate:
                    if detected_plate in detected_plates.keys():
                        detected_plates[detected_plate] +=1
                        with open(f"{plate_detection_output_path}detection_counter.json", "w") as file:
                            # file.write(f"{str(detected_plates)}\n")
                            json.dump(detected_plates, file)
                        if detected_plates[detected_plate] > 5:
                            publish(plate= detected_plate)
                            print(200*'*')
                            
                    else:
                        detected_plates[detected_plate] = 1
                new_name = get_new_name()
                # print(new_name)
                b = cv2.imwrite(f"{save_dir}{new_name}.png", frame)
                
        except KeyboardInterrupt:
            pass
        finally:
            cv2.destroyAllWindows()

if __name__ == '__main__':
    stream_camera()
