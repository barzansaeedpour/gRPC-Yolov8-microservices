import shutil
import grpc
import cv2
import Camera_pb2
import Camera_pb2_grpc
import numpy as np
from datetime import datetime
import os
from dotenv import find_dotenv, load_dotenv
import json
from my_yolo_v8.yolov8 import plate_detection
from my_yolo_v8.rabbitmq.publisher import publish
import io, base64
from PIL import Image


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
                new_name = get_new_name()
                b = cv2.imwrite(f"{save_dir}{new_name}.png", frame)
                yield frame

        except KeyboardInterrupt:
            return None
        finally:
            cv2.destroyAllWindows()

