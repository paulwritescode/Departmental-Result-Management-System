from flask_sqlalchemy import SQLAlchemy
from . import db,login_manager
from datetime import datetime
from flask_login import UserMixin
# class Users(db.Model):
#     __tablename__="Users"

#     id=db.Column(db.Integer,primary_key=True)
#     fname=db.Column(db.String(16),nullable=False)
#     mname=db.Column(db.String(16),nullable=False)
#     email=db.Column(db.String(120),nullable=False)
#     roll=db.Column(db.String(8),nullable=False)
#     password=db.Column(db.String,nullable=False)
#     Department_id=db.Column(db.Integer, nullable=False)
#     Eyear=db.Column(db.Integer,nulable=True)
#     Module=db.Column(db.String(length=3),nullable=True)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    fname = db.Column(db.String(255), nullable = False)
    lname = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(255), nullable = False)
    username = db.Column(db.String(255), nullable = False)
    role = db.Column(db.String(255), nullable = False)
    password = db.Column(db.String(255), nullable = False)
    status = db.Column(db.Integer, default = 0, nullable = False)



    def _repr_(self):
        return f'User("{self.id}","{self.fname}","{self.lname}","{self.email}","{self.edu}","{self.username}","{self.status}")'
@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))    


