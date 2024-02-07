from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,validators,EmailField
from wtforms.validators import InputRequired,Email,Length,ValidationError


    # id=db.Column(db.Integer,primary_key=True)
    # fname=db.Column(db.String(16),nullable=False)
    # mname=db.Column(db.String(16),nullable=False)
    # email=db.Column(db.String(120),nullable=False)
    # roll=db.Column(db.String(8),nullable=False)
    # password=db.Column(db.String,nullable=False)
    # Department_id=db.Column(db.Integer, nullable=False)
    # Eyear=db.Column(db.Integer,nulable=True)
    # Module=db.Column(db.String(length=3),nullable=True)
class RegisterForm(FlaskForm):
