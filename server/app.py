import grpc
import cv2
import time
from concurrent import futures
import camera_pb2
import camera_pb2_grpc
from datetime import datetime
import shutil
import os

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
        video_path = '/code/files/video_test.mp4'
        saved_images = '/code/saved_images/'
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

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    camera_pb2_grpc.add_CameraServicer_to_server(CameraServicer(), server)
    # server.add_insecure_port('[::]:50051')
    server.add_insecure_port('0.0.0.0:50051')
    # server.add_insecure_port('127.0.0.1:50051')
    server.start()
    print("Server started on port 50051")
    try:
        while True:
            time.sleep(60 * 60 * 24)  # Keep server running
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()

