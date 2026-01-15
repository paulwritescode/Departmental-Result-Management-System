from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, StringField, SubmitField,SelectField
from wtforms.validators import DataRequired, NumberRange
# from ..models import User,Modules,Units
from app.models import User,Units,Modules


class EnrollStudentForm(FlaskForm):
    # student_id = IntegerField("Student ID", validators=[DataRequired()])
    student_id=SelectField('Students',coerce=int)
    # module_id = IntegerField("Module ID", validators=[DataRequired()])
    module_id = SelectField('Modules',coerce=int)
    academic_year = IntegerField("Academic Year", validators=[DataRequired()])
    submit = SubmitField("Enroll")
    def __init__(self, *args, **kwargs):
        super(EnrollStudentForm, self).__init__(*args, **kwargs)

        self.student_id.choices=[(students.id, f"{students.fname} {students.lname}- {students.Reg_no}" ) 
                                for students in User.query.filter(User.role_id == "1").all()]
        self.module_id.choices=[(students.id, f"{students.name} {students.year} year -{students.semester} semester" ) 
                                for students in Modules.query.all()]


class AssignUnitForm(FlaskForm):
    # lecturer_id = IntegerField("Lecturer ID", validators=[DataRequired()])
    lecturer_id = SelectField('Lecturers',coerce=int)
    # unit_id = IntegerField("Unit ID", validators=[DataRequired()])
    unit_id = SelectField('Unit ID',coerce=int)
    academic_year = IntegerField("Academic Year", validators=[DataRequired()])
    submit = SubmitField("Assign")
    def __init__(self, *args, **kwargs):
        super(AssignUnitForm, self).__init__(*args, **kwargs)

        self.lecturer_id.choices=[(students.id, f"{students.fname} {students.lname} {students.Reg_no}" ) 
                                for students in User.query.filter(User.role_id==2).all()]
        self.unit_id.choices=[(students.id, f"{students.name} {students.code} {students.module_id}" ) 
                                for students in Units.query.all()]


class AddUnit(FlaskForm):
    unit_name = StringField("Unit Name", validators=[DataRequired()])
    unit_code = IntegerField("Unit Code", validators=[DataRequired()])
    module_id = IntegerField("Module ID", validators=[DataRequired()])
    submit = SubmitField("Add Unit")

