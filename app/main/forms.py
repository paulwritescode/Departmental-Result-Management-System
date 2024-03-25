# forms.py

from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class EnrollStudentForm(FlaskForm):
    student_id = IntegerField("Student ID", validators=[DataRequired()])
    module_id = IntegerField("Module ID", validators=[DataRequired()])
    academic_year = IntegerField("Academic Year", validators=[DataRequired()])
    submit = SubmitField("Enroll")


class AssignUnitForm(FlaskForm):
    lecturer_id = IntegerField("Lecturer ID", validators=[DataRequired()])
    unit_id = IntegerField("Unit ID", validators=[DataRequired()])
    academic_year = IntegerField("Academic Year", validators=[DataRequired()])
    submit = SubmitField("Assign")


class MarksInputForm(FlaskForm):
    cat_marks = FloatField("CAT Marks")
    assignment_marks = FloatField("Assignment Marks")
    main_exam_marks = FloatField("Main Exam Marks")
    submit = SubmitField("Submit")


class AddMarksForm(FlaskForm):
    cat_marks = FloatField(
        "CAT Marks", validators=[DataRequired(), NumberRange(min=0, max=100)]
    )
    assignment_marks = FloatField(
        "Assignment Marks", validators=[DataRequired(), NumberRange(min=0, max=100)]
    )
    practical_marks = FloatField(
        "Practical Marks", validators=[DataRequired(), NumberRange(min=0, max=100)]
    )
    exam_marks = FloatField(
        "Exam Marks", validators=[DataRequired(), NumberRange(min=0, max=100)]
    )
    submit = SubmitField("Add Marks")
