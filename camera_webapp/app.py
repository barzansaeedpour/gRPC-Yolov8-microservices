

from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
from datetime import datetime
import os
from dotenv import find_dotenv, load_dotenv
import psycopg2
from token_claim_validation import token_claim_validation

print(200*"*")

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
base_dir = os.getenv("base_dir_camera_webapp")
camera_webapp_address = os.getenv("camera_webapp_address")
# postgresql_user = os.getenv("postgresql_user")
# postgresql_password = os.getenv("postgresql_password")
postgresql_user = "postgres"
postgresql_password = "postgres"
debug = os.getenv("debug")

print(base_dir)

# x = 1/0
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{base_dir}/test.db' # Three forwarded slashes mean a relative path and four mean an absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{postgresql_user}:{postgresql_password}@localhost'
print(33*postgresql_password)
db = SQLAlchemy(app)

####################################
def fill_database():
    old_claims = Claim.query.all()
    old_claims = [c.title for c in old_claims]
    print(old_claims)
    
    new_claims = [
    "camera_webapp/camera/post",
    "camera_webapp/camera/get",
    "camera_webapp/camera/delete",
    "camera_webapp/camera/update"
    ]
    
    for claim in new_claims:
        if claim not in old_claims:
            new_claim = Claim(title=claim) 
            db.session.add(new_claim)
    db.session.commit()      
####################################


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
    
     # Define a unique constraint on the 'title' column
    __table_args__ = (UniqueConstraint('title'),)
    
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

@app.route('/claims', methods= ['POST', 'GET', 'DELETE'])
def claims():
    claims = Claim.query.all()
    if request.method == 'DELETE':
        # bool = token_claim_validation(token=token, claim = 'camera_webapp/camera/delete')
        # if True:
        claims_to_delete = request.json['claims']
        for claim in claims:
            for claim_to_delete in claims_to_delete:
                if claim.title == claim_to_delete:
                    db.session.delete(claim)
        db.session.commit()
        return Status(message='عملیات با موفقیت انجام شد', isSuccess=True, statusCode=200).success() 
    elif request.method == 'GET':
        claims_list = []
        for claim in claims:
            claims_list.append({
                'id': claim.id,
                'title': claim.title,
            })
        return jsonify(claims_list)
    elif request.method == 'POST':
        claims_to_add = request.json['claims']
        print('***claims***')
        print(claims)
        for claim in claims_to_add:
            if not claim in [c.title for c in claims]:
                new_claim = Claim(title=claim) 
                db.session.add(new_claim)
        db.session.commit()      
        return Status(message='عملیات با موفقیت انجام شد', isSuccess=True, statusCode=200).success() 
        # new_task = Claim(content = claims)
    # else:
    return Status(message='خطا در گرفتن سطوح دسترسی', isSuccess=False, statusCode=400).error()


@app.route('/cameras', methods= ['POST', 'GET', 'DELETE', 'PUT'])
def cameras():
    
    token = request.authorization.token
    
    cameras = Camera.query.all()
    if request.method == 'DELETE':
        # bool = token_claim_validation(token=token, claim = 'camera_webapp/camera/delete')
        if True:
            print(89*'h')
            cameras = request.json['cameras']
            for camera in cameras:
                camera_to_delete = Camera.query.get_or_404(camera) 
                db.session.delete(camera_to_delete)
            db.session.commit()
            return Status(message='عملیات با موفقیت انجام شد', isSuccess=True, statusCode=200).success() 
        else:
            return Status(message='خطا در توکن یا عدم سطح دسترسی', isSuccess=False, statusCode=400).error()
    if request.method == 'GET':
        bool = token_claim_validation(token=token, claim = 'camera_webapp/camera/get')
        if bool:
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
        else:
            return Status(message='خطا در توکن یا عدم سطح دسترسی', isSuccess=False, statusCode=400).error()
        
    elif request.method == 'POST':
        bool = token_claim_validation(token=token, claim = 'camera_webapp/camera/post')
        if bool:
            cameras = request.json['cameras']
            for camera in cameras:
                new_camera = Camera(title=camera['title'], ip=camera['ip'], port= camera["port"], connection_string=camera["connection_string"]) 
                db.session.add(new_camera)
            db.session.commit()
            return cameras
        else:
            return Status(message='خطا در توکن یا عدم سطح دسترسی', isSuccess=False, statusCode=400).error()
    
    elif request.method == 'PUT':
        bool = token_claim_validation(token=token, claim = 'camera_webapp/camera/update')
        if bool:
            camera = request.json
            camera_to_update = Camera.query.get_or_404(camera["id"])
            camera_to_update.title = camera['title']
            camera_to_update.port = camera['port']
            camera_to_update.connection_string = camera['connection_string']
            # for camera in cameras:
            #     new_camera = Camera(title=camera['title'], ip=camera['ip'], port= camera["port"], connection_string=camera["connection_string"]) 
            #     db.session.add(new_camera)
            db.session.commit()
            return camera
        else:
            return Status(message='خطا در توکن یا عدم سطح دسترسی', isSuccess=False, statusCode=400).error()
            
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
    print(30*"main")
    app.run(debug=True) 
    with app.app_context():
        db.create_all()
        fill_database()
    app.run(debug=debug)
    