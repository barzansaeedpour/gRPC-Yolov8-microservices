import grpc
import cv2
import camera_pb2
import camera_pb2_grpc
import numpy as np
from datetime import datetime
import os
from my_yolo_v8.yolov8 import plate_detection
###################################################
from flask import Flask, request,jsonify
from flask_socketio import SocketIO,emit
from flask_cors import CORS
######################################

save_dir = '/code/saved_images/'
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


#################################################### Flask webapp
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app,cors_allowed_origins="*")

@app.route("/")
def index():
    data = {'data':'The index page'}
    return jsonify(data)

@app.route("/http-call")
def http_call():
    """return JSON with string data as the value"""
    data = {'data':'This text was fetched using an HTTP call to server on render'}
    return jsonify(data)

@socketio.on("connect")
def connected():
    """event listener when client connects to the server"""
    print(request.sid)
    print("client has connected")
    emit("connect",{"data":f"id: {request.sid} is connected"})

@socketio.on('data')
def handle_message(data):
    """event listener when client types a message"""
    print("data from the front end: ",str(data))
    emit("data",{'data':data,'id':request.sid},broadcast=True)
    

@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    print("user disconnected")
    emit("disconnect",f"user {request.sid} disconnected",broadcast=True)



def stream_camera():
    with grpc.insecure_channel("camera-service-server:50051") as channel:
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
                plate_detection(frame)
                new_name = get_new_name()
                # print(new_name)
                b = cv2.imwrite(f"{save_dir}{new_name}.png", frame)
                
        except KeyboardInterrupt:
            pass
        finally:
            cv2.destroyAllWindows()

if __name__== "__main__":
    # socketio.run(app,debug=True,port=5001)
    stream_camera()
    
