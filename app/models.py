from flask_sqlalchemy import SQLAlchemy
from . import db,login_manager
from datetime import datetime
from flask import current_app
from sqlalchemy import event
from sqlalchemy.event import listens_for
from flask_login import UserMixin,AnonymousUserMixin

class User(db.Model,UserMixin):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key = True)
    fname = db.Column(db.String(255), nullable = False)
    lname = db.Column(db.String(255), nullable = False)
    email = db.Column(db.String(255), nullable = False)
    username = db.Column(db.String(255), nullable = False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    phone=db.Column(db.Integer, unique=True)
    Reg_no=db.Column(db.String(10),unique=True)
    Year_of_Registration=db.Column(db.Integer)
    password = db.Column(db.String(255), nullable = False)
    status = db.Column(db.Integer, default = 0, nullable = False)
    current_module=db.Column(db.Integer,db.ForeignKey('modules.id'),nullable=True)
    student_enrollments = db.relationship('StudentEnrollment', backref='student', lazy='dynamic')
    lecturer_unit_assignment = db.relationship('LecturerAssignment', backref='lecturer', lazy='dynamic')


    
    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        if self.role is None:
            if self.email==current_app.config['FLASKY_ADMIN']:
                self.role=Role.query.filter_by(name="Administartor").first()
                if self.role is None:
                    self.role=Role.query.filter_by(default=True).first() 
    def __repr__(self):
        return f'User("{self.id}","{self.fname}","{self.lname}","{self.email}","{self.edu}","{self.username}","{self.status}")'
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
    users=db.relationship(User,backref='role',lazy='dynamic')
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

class Units (db.Model):
    __tablename__="units"

    id =db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20),nullable=False)
    code=db.Column(db.Integer,unique=True,nullable=False)
    module_id=db.Column(db.Integer,db.ForeignKey('modules.id'))
    student_enrollments = db.relationship('EnrollmentUnits', backref='student_units', lazy='dynamic', overlaps="student_enrollments,student_units")
    unit_lecturer = db.relationship('LecturerAssignment', backref='lecs', lazy='dynamic')
   

    @staticmethod
    def insert_units():
        units_data=[
            ("Calculus 1",1101,1),
            ("Electricity and Magnetism ",1102,1),
            ("Computing mathematics",1103,1),
            ("Calculus 2 ",1201,2),
            ("Probability and Statistics 1",1202,2),
            ("Introduction to Computer Science",1203,2),
            ("Probability and Statistics 2",2101,3),
            ("Database Systems",2102,3),
            ("System Design",2103,3),
            ("Introduction to Programming", 2201,4),
            ("Programming Concepts",2202,4),
            ("Vectors",2203,4),
            ("Theory of Computing",3101,5),
            ("Computer Graphics",3102,5),
            ("Operating Systems",3103,5),
            ("Compiler Construction",3201,6),
            ("Multimedia Systems",3202,6),
            ("Networking",3203,6),
            ("Computer Security",4101,7),
            ("Machine Learning",4102,7),
            ("Human Computer Interaction",4103,7),
            ("Embedded Systems",4201,8),
            ("Enterpreneurship",4202,8),
            ("Professional Ethics",4203,8)

        ]
        for name, code, module_id in units_data:
            unit = Units(name=name, code=code, module_id=module_id)
            db.session.add(unit)

        db.session.commit()




class Modules(db.Model):
    __table__name="modules"
    
    id =db.Column(db.Integer,unique=True,primary_key=True)
    name=db.Column(db.String(20),nullable=False)
    year=db.Column(db.Integer,nullable=False)
    semester=db.Column(db.Integer,nullable=False)
    code=db.Column(db.Integer,unique=True,nullable=False)
    student_enrollments = db.relationship('StudentEnrollment', backref='module', lazy='dynamic')
    unit_module=db.relationship('Units', backref='unit_module', lazy='dynamic')



# ... (existing code)

class StudentEnrollment(db.Model):
    __tablename__="student_enrollment"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    academic_year = db.Column(db.Integer,nullable=False)
    # enrollment = db.relationship('StudentEnrollment', backref='marks', lazy=True)
    units = db.relationship('Units', secondary='enrollment_units', backref='enrollments', lazy='dynamic', overlaps="student_enrollments,student_units")
    

class EnrollmentUnits(db.Model):
    __tablename__ = 'enrollment_units'
    id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('student_enrollment.id'))
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'))
    unit_marks=db.relationship("Marks",backref="unit_marks",lazy="dynamic")
    nonsense=db.Column(db.String,nullable=True)
   

# ... (existing code)
class LecturerAssignment(db.Model):
    __tablename__="lecturer_assignment"
    id = db.Column(db.Integer, primary_key=True)
    lecturer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=False)
    academic_year = db.Column(db.Integer,nullable = False)



class Marks(db.Model):
    __tablename__="marks"
    id = db.Column(db.Integer, primary_key=True)
    enrollment_id = db.Column(db.Integer, db.ForeignKey('enrollment_units.id'), nullable=False)
    cat_marks = db.Column(db.Float)
    assignment_marks = db.Column(db.Float)
    practical_marks = db.Column(db.Float)
    exam_marks = db.Column(db.Float)
    overall_marks = db.Column(db.Float)
    status = db.Column(db.String(20))  

 
