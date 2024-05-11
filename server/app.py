import grpc
import cv2
import time
from concurrent import futures
import camera_pb2
import camera_pb2_grpc
import auth_pb2
import auth_pb2_grpc
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
            
class AuthServicer(auth_pb2_grpc.AuthServicer):
    def GetClaims(self, request_iterator, context):
        claims = [
            auth_pb2.Claim(title="add_cameraaaa"),
            auth_pb2.Claim(title="remove_cameraaaa"),
        ]
        print("claims")
        return auth_pb2.GetClaimsResponse(claims=claims)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # camera_pb2_grpc.add_CameraServicer_to_server(CameraServicer(), server)
    auth_pb2_grpc.add_AuthServicer_to_server(AuthServicer, server)
    # server.add_insecure_port('[::]:50051')
    server.add_insecure_port('0.0.0.0:81')
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


#################################################### Flask webapp


# from flask import Flask, render_template, request, redirect, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime


# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # Three forwarded slashes mean a relative path and four mean an absolute path
# db = SQLAlchemy(app)

# class Status():
#     def __init__(self, message, statusCode, isSuccess) -> None:
#         self.message = message
#         self.statusCode = statusCode
#         self.isSuccess = isSuccess
        
#     def error(self):
#         return {"message":self.message, "statusCode": self.statusCode, "isSuccess": self.isSuccess}

# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     content = db.Column(db.String(200), nullable = False)
#     completed = db.Column(db.Integer, default = 0)
#     date_created = db.Column(db.DateTime, default = datetime.now())

#     def __repr__(self):
#         return '<Task %r' % self.id
    
# class Claim(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     title = db.Column(db.String(200), nullable = False)
    
#     def __repr__(self):
#         return '<Claim %r' % self.id
    
# class Camera(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     title = db.Column(db.String(200), nullable = False)
    
#     def __repr__(self):
#         return '<Claim %r' % self.id



# @app.route('/', methods= ['POST', 'GET'])
# def index():
#     if request.method == 'POST':
#         task_content = request.form['content']
#         new_task = Todo(content = task_content)
#         try: 
#             db.session.add(new_task)
#             db.session.commit()
#             return redirect('/')
#         except:
#             return "There was an issue adding your task"
#     else:
#         tasks = Todo.query.order_by(Todo.date_created).all()
#         return render_template('index.html', tasks= tasks)

# @app.route('/claims', methods= ['POST', 'GET'])
# def claims():
#     claims = Claim.query.all()
#     if request.method == 'GET':
#         claims_list = []
#         for claim in claims:
#             claims_list.append({
#                 'id': claim.id,
#                 'title': claim.title,
#             })
#         return jsonify(claims_list)
#     elif request.method == 'POST':
#         claims = request.json['claims']
#         print('***claims***')
#         print(claims)
#         for claim in claims:
#             new_claim = Claim(title=claim) 
#             db.session.add(new_claim)
#         db.session.commit()       
#         return claims
#         # new_task = Claim(content = claims)
#     # else:
#     return Status(message='خطا در گرفتن سطوح دسترسی', isSuccess=False, statusCode=400).error()
    
#     # if request.method == 'POST':
#     #     task_content = request.form['content']
#     #     new_task = Todo(content = task_content)
#     #     try: 
#     #         db.session.add(new_task)
#     #         db.session.commit()
#     #         return redirect('/')
#     #     except:
#     #         return "There was an issue adding your task"
#     # else:
#     #     tasks = Todo.query.order_by(Todo.date_created).all()
#     #     return render_template('index.html', tasks= tasks)

# @app.route('/delete/<int:id>')
# def delete(id):
#     task_to_delete = Todo.query.get_or_404(id)
#     try:
#         db.session.delete(task_to_delete)
#         db.session.commit()
#         return redirect('/')
#     except:
#         return "There was an issue deleting that task"
    
# @app.route('/update/<int:id>', methods= ['POST', 'GET'])
# def update(id):
#     task_to_update = Todo.query.get_or_404(id)
#     if request.method == "POST":
#         task_to_update.content = request.form['content']
#         try:
#             db.session.commit()
#             return redirect('/')
#         except:
#             return "There was an issue updating that task"
        
#     else:
#         return render_template('update.html', task= task_to_update)

# if __name__ == "__main__":
#     # app.run(debug=True) 
#     with app.app_context():
#         db.create_all()
#     app.run(debug=False, host='0.0.0.0')
    


