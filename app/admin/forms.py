from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField,FloatField
from wtforms.validators import DataRequired,NumberRange

class EnrollStudentForm(FlaskForm):
    student_id = IntegerField('Student ID', validators=[DataRequired()])
    module_id = IntegerField('Module ID', validators=[DataRequired()])
    academic_year = IntegerField('Academic Year', validators=[DataRequired()])
    submit = SubmitField('Enroll')

class AssignUnitForm(FlaskForm):
    lecturer_id = IntegerField('Lecturer ID', validators=[DataRequired()])
    unit_id = IntegerField('Unit ID', validators=[DataRequired()])
    academic_year = IntegerField('Academic Year', validators=[DataRequired()])
    submit = SubmitField('Assign')