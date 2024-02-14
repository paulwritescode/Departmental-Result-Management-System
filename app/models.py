<<<<<<< HEAD
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from . import db

=======
from flask_sqlalchemy import SQLAlchemy
from . import db,login_manager
from datetime import datetime
from flask import current_app
from flask_login import UserMixin,AnonymousUserMixin
>>>>>>> refs/remotes/origin/main
# class Users(db.Model):
#     __tablename__="Users"

#     id=db.Column(db.Integer,primary_key=True)
#     fname=db.Column(db.String(16),nullable=False)
#     mname=db.Column(db.String(16),nullable=False)
#     email=db.Column(db.String(120),nullable=False)
#     roll=db.Column(db.String(8),nullable=False)
#     password=db.Column(db.String,nullable=False)
#     Department_id=db.Column(db.Integer, nullable=False)
#     year=db.Column(db.Integer,nullable=True)
#     Module=db.Column(db.String(length=3),nullable=True)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    fname = db.Column(db.String(255), nullable = False)
    lname = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(255), nullable = False)
    username = db.Column(db.String(255), nullable = False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password = db.Column(db.String(255), nullable = False)
    status = db.Column(db.Integer, default = 0, nullable = False)
    
    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        if self.role is None:
            if self.email==current_app.config['FLASKY_ADMIN']:
                self.role=Role.query.filter_by(name="Administartor").first()
                if self.role is None:
                    self.role=Role.query.filter_by(default=True).first() 
    def __repr__(self):
        return f'User("{self.id}","{self.fname}","{self.lname}","{self.email}","{self.edu}","{self.username}","{self.status}")'
<<<<<<< HEAD

=======
    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)
    def is_administartor(self):
        return self.can(Permission.Admin)
@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))   

    
            
  
    
class AnonymousUser(AnonymousUserMixin):
    def can (self,permissions):
        return False
    def is_administartor(self):
        return False
login_manager.anonymous_user=AnonymousUser
    
>>>>>>> refs/remotes/origin/main


# Permissions class defination 
class Permission:
    VIEW=1
    COMMENT=2
    WRITE=4
    EDIT=8
    ADMIN=16 

# Roles Table defined Here 
class Role(db.Model):
    __tablename__="roles"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    default=db.Column(db.Boolean,default=False,index=True)
    permissions=db.Column(db.Integer)
    users=db.Relationship(User,backref='role',lazy='dynamic')
    def __init__(self,**kwargs):
        super(Role,self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions=0


    def add_permission(self,perm):
        if not self.has_permission(perm):
            self.permission=+perm
    def remove_pemision(self,perm):
        if self.has_permission(perm):
            self.permisions=-perm
    def reset_permissons(self):
        self.permission=0
    def has_permission(self, perm):
     return self.permissions & perm == perm

    
# Assigning Permissions to Roles
    @staticmethod
    def insert_roles():        
        roles={
            'User': [Permission.VIEW,Permission.COMMENT],
            'Lecturer':[Permission.VIEW,Permission.COMMENT,Permission.WRITE],
            'ADMIN':[Permission.VIEW,Permission.COMMENT,Permission.WRITE,Permission.EDIT,Permission.ADMIN]
        }
        default_role='User'
        for r in roles:
            role=Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissons()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default=(role.name==default_role)
            db.session.add(role)
        db.session.commit()











