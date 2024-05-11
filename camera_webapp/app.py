

from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
base_dir = os.getenv("base_dir_camera_webapp")

print(base_dir)

# x = 1/0
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{base_dir}test.db' # Three forwarded slashes mean a relative path and four mean an absolute path
db = SQLAlchemy(app)

class Status():
    def __init__(self, message, statusCode, isSuccess) -> None:
        self.message = message
        self.statusCode = statusCode
        self.isSuccess = isSuccess
        
    def error(self):
        return {"message":self.message, "statusCode": self.statusCode, "isSuccess": self.isSuccess}
    def success(self):
        return {"message":self.message, "statusCode": self.statusCode, "isSuccess": self.isSuccess}

# class Todo(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#     content = db.Column(db.String(200), nullable = False)
#     completed = db.Column(db.Integer, default = 0)
#     date_created = db.Column(db.DateTime, default = datetime.now())

#     def __repr__(self):
#         return '<Task %r' % self.id
    
class Claim(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    
    def __repr__(self):
        return '<Claim %r' % self.id
    
class Camera(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    ip = db.Column(db.String(200), nullable = True)
    port = db.Column(db.String(200), nullable = True)
    connection_string = db.Column(db.String(200), nullable = False)
    
    def __repr__(self):
        return '<Claim %r' % self.id


@app.route('/', methods= ['POST', 'GET'])
def index():
    return "Okay"
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

@app.route('/claims', methods= ['POST', 'GET'])
def claims():
    claims = Claim.query.all()
    if request.method == 'GET':
        claims_list = []
        for claim in claims:
            claims_list.append({
                'id': claim.id,
                'title': claim.title,
            })
        return jsonify(claims_list)
    elif request.method == 'POST':
        claims = request.json['claims']
        print('***claims***')
        print(claims)
        for claim in claims:
            new_claim = Claim(title=claim) 
            db.session.add(new_claim)
        db.session.commit()      
        return claims
        # new_task = Claim(content = claims)
    # else:
    return Status(message='خطا در گرفتن سطوح دسترسی', isSuccess=False, statusCode=400).error()

@app.route('/cameras', methods= ['POST', 'GET', 'DELETE'])
def cameras():
    cameras = Camera.query.all()
    if request.method == 'DELETE':
        cameras = request.json['cameras']
        for camera in cameras:
            camera_to_delete = Camera.query.get_or_404(camera) 
            db.session.delete(camera_to_delete)
        db.session.commit()
        return Status(message='عملیات با موفقیت انجام شد', isSuccess=True, statusCode=200).success() 
    if request.method == 'GET':
        camera_list = []
        for camera in cameras:
            camera_list.append({
                'id': camera.id,
                'title': camera.title,
                'ip': camera.ip,
                'port': camera.port,
                'connection_string': camera.connection_string,
            })
        return jsonify(camera_list)
    
    elif request.method == 'POST':
        cameras = request.json['cameras']
        for camera in cameras:
            new_camera = Camera(title=camera['title'], ip=camera['ip'], port= camera["port"], connection_string=camera["connection_string"]) 
            db.session.add(new_camera)
        db.session.commit()       
        return cameras
        
    return Status(message='خطا در گرفتن لیست دوربین ها', isSuccess=False, statusCode=400).error()

# @app.route('/delete_camera/<int:id>', methods=['DELETE'])
# def delete_camera(id):
#     camera_to_delete = Camera.query.get_or_404(id)
#     try:
#         db.session.delete(camera_to_delete)
#         db.session.commit()
#         return redirect('/cameras')
#     except:
#         return Status(message='خطا در حذف دوربین', isSuccess=False, statusCode=400).error()
    
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

if __name__ == "__main__":
    # app.run(debug=True) 
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
    