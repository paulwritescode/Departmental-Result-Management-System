from flask_wtf import FlaskForm
from wtforms import (
    EmailField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    validators,
)
from wtforms.validators import (
    DataRequired,
    Email,
    InputRequired,
    Length,
    NumberRange,
    ValidationError,
)

from ..models import User


# id=db.Column(db.Integer,primary_key=True)
# Eyear=db.Column(db.Integer,nulable=True)
# Module=db.Column(db.String(length=3),nullable=True)
class RegisterForm(FlaskForm):
    fname = StringField(
        validators=[InputRequired(), Length(max=10, min=3)],
        render_kw={"placeholder": "First Name"},
    )
    lname = StringField(
        validators=[InputRequired(), Length(max=10, min=3)],
        render_kw={"placeholder": "First Name"},
    )
    role = IntegerField(validators=[InputRequired()])
    
 
    password = PasswordField(
        validators=[InputRequired(), Length(max=10, min=5)],
        render_kw={"placeholder": "password"},
    )
    email = EmailField(
        validators=[Email(), InputRequired()],
        render_kw={"placeholder": "abcd@gmail.com"},


        
    )
    username = StringField(
        validators=[InputRequired(), Length(max=10, min=4)],
        render_kw={"placeholder": "User Name"},
    )
    submit = SubmitField("Submit")

    def validate_username(self, username):
        existing_username = User.query.filter_by(username=username.data).first()

        if existing_username:
            raise ValidationError("The username already exists try another username")

    def validate_email(self, email):
        existing_email = User.query.filter_by(email=email.data).first()

        if existing_email:
            raise ValidationError(
                "The email" + email + " already exists try another email"
            )


class LoginForm(FlaskForm):
    email = EmailField(
        validators=[Email(), InputRequired()],
        render_kw={"placeholder": "Enter usermail"},
    )
    password = PasswordField(
        validators=[InputRequired(), Length(max=10, min=5)],
        render_kw={"placeholder": "Enter password"},
    )
    submit = SubmitField("Submit")


    class AddUnitForm(FlaskForm):
        name=StringField(
        validators=[InputRequired(), Length(max=10, min=4)],
        render_kw={"placeholder": "Unit Name"},)
        code=IntegerField()
        module_id=IntegerField()
        submit=SubmitField("Add Unit")



