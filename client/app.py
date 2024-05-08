import grpc
import cv2
import camera_pb2
import camera_pb2_grpc
import numpy as np
from datetime import datetime
import os
import json
from my_yolo_v8.yolov8 import plate_detection
from my_yolo_v8.rabbitmq.publisher import publish
###################################################
# from flask import Flask, request, jsonify
# from flask_socketio import SocketIO, emit
# from flask_cors import CORS
######################################

base_dir = ''


save_dir = '/code/saved_images/'
plate_detection_output_path = "/code/my_yolo_v8/outputs/"


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

#################################################### Flask webapp


from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # Three forwarded slashes mean a relative path and four mean an absolute path
db = SQLAlchemy(app)

class Status():
    def __init__(self, message, statusCode, isSuccess) -> None:
        self.message = message
        self.statusCode = statusCode
        self.isSuccess = isSuccess
        
    def error(self):
        return {"message":self.message, "statusCode": self.statusCode, "isSuccess": self.isSuccess}

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default = 0)
    date_created = db.Column(db.DateTime, default = datetime.now())

    def __repr__(self):
        return '<Task %r' % self.id
    
class Claim(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    
    def __repr__(self):
        return '<Claim %r' % self.id



@app.route('/', methods= ['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content = task_content)
        try: 
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks= tasks)

@app.route('/claims', methods= ['POST', 'GET'])
def claims():
    if request.method == 'GET':
        claims = Claim.query.all()
        return claims
    elif request.method == 'POST':
        claims = request.json['claims']
        print('***claims***')
        print(claims)
        for claim in claims:
            new_claim = Claim(title=claim) 
            db.session.add(new_claim)
        db.session.commit()       
        return {"success"}
        # new_task = Claim(content = claims)
    # else:
    return Status(message='خطا در گرفتن سطوح دسترسی', isSuccess=False, statusCode=400).error()
    
    # if request.method == 'POST':
    #     task_content = request.form['content']
    #     new_task = Todo(content = task_content)
    #     try: 
    #         db.session.add(new_task)
    #         db.session.commit()
    #         return redirect('/')
    #     except:
    #         return "There was an issue adding your task"
    # else:
    #     tasks = Todo.query.order_by(Todo.date_created).all()
    #     return render_template('index.html', tasks= tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an issue deleting that task"
    
@app.route('/update/<int:id>', methods= ['POST', 'GET'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)
    if request.method == "POST":
        task_to_update.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue updating that task"
        
    else:
        return render_template('update.html', task= task_to_update)

if __name__ == "__main__":
    # app.run(debug=True) 
    with app.app_context():
        db.create_all()
    app.run(debug=False, host='0.0.0.0')
    


