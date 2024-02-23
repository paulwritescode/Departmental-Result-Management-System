from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)

from .. import db
from ..decorators import admin_required, permission_required
from ..models import (EnrollmentUnits, LecturerAssignment, Marks, Modules,
                      Permission, StudentEnrollment, Units, User)
from . import main
from .forms import *


@main.route('/')
@login_required
@permission_required(Permission.VIEW)
def home():
  if current_user.is_authenticated and current_user.role.name == 'Lecturer':
    lecturer_id = current_user.id

    # Now you can use the lecturer_id in your queries or any other logic
    # For example, querying for units assigned to the lecturer
    assigned_units = (
        LecturerAssignment.query
        .filter_by(lecturer_id=lecturer_id)
        .with_entities(LecturerAssignment.unit_id, LecturerAssignment.academic_year)
        .all()
    )

    if assigned_units:
        print("There exists permission for",current_user.username)
        enrolled_students = []

        for assigned_unit in assigned_units:
            academic_year = assigned_unit.academic_year
            unit_id = assigned_unit.unit_id
            query=db.session.query(
                EnrollmentUnits,
                User.fname.label('student_fname'),
                User.lname.label("student_lname"),
                User.Reg_no.label("student_regNo"),
                Units.name.label("unit_name"),
                Units.code.label("unit_code"),
                EnrollmentUnits.id.label("unitenrollment_id"),
                EnrollmentUnits.enrollment_id.label("studentEnrollment_id"),
                StudentEnrollment.academic_year.label("academicYear")
                ).join(
                    StudentEnrollment,EnrollmentUnits.enrollment_id==StudentEnrollment.id
                ).join(
                    User,StudentEnrollment.student_id==User.id
                ).join(
                    Units, EnrollmentUnits.unit_id==Units.id
                )
            enrolledStudents=query.filter(Units.id == unit_id,
                    StudentEnrollment.academic_year == academic_year)
            students=enrolledStudents.all()

            InMyUnit=[]
            for student_data in students:
                print(student_data)


            # for student_fname,student_lname,unit_name,unit_code,unitenrollment_id,academicYear,student_regNo in students:
            #      InMyUnit.append({
            #         "enrollment_id":unitenrollment_id,
            #         "student_name": student_fname + student_lname,
            #         "course_name": unit_name,
            #         "course_code": unit_code,
            #         "student_reg": student_regNo,
            #         "academicYear":academicYear
            #                  })


            # students = (
            #     User.query
            #     .join(StudentEnrollment)
            #     .join(EnrollmentUnits)
            #     .join(Units)
            #     .add_columns(
            #         User.id.label('user_id'),
            #         User.fname,
            #         User.lname,
            #         User.email,
            #         Units.name.label('unit_name'),
            #         Units.code.label('unit_code')
            #     )
            #     .filter(
            #         Units.id == unit_id,
            #         StudentEnrollment.academic_year == academic_year
            #     )
            #     .all()
            # )

            # enrolled_students.extend(students)

            # for student in enrolled_students:
            #     print(f"Student ID: {student.user_id}, Name: {student.fname} {student.lname}, Email: {student.email}, Unit: {student.unit_name}, Code: {student.unit_code}")

    return render_template("user/index.html" title= )




# TODO Move to admin under templates (this is the admin enrolling students)
@main.route('/enroll_student', methods=['GET', 'POST'])
def enroll_student():
    form = EnrollStudentForm()
    if form.validate_on_submit():
        student_id = form.student_id.data
        module_id = form.module_id.data
        academic_year = form.academic_year.data

        # Check if the student is not already enrolled in the module
        enrollment_exists = StudentEnrollment.query.filter_by(student_id=student_id, module_id=module_id,academic_year=academic_year).first()
        if enrollment_exists:
            flash('Student is already enrolled in the module.', 'warning')
        else:
            # Create a new enrollment
            new_enrollment = StudentEnrollment(student_id=student_id, module_id=module_id, academic_year=academic_year)

            db.session.add(new_enrollment)
            db.session.commit()
            new_enrollment_id = new_enrollment.id
            enroll_units=Units.query.filter_by(module_id=module_id).all()
            print(enroll_units[0].id)
            y=2
            for unit in enroll_units:
                new_unit_enrollment=EnrollmentUnits(enrollment_id=new_enrollment_id,unit_id=unit.id)
                print(new_unit_enrollment)
                db.session.add(new_unit_enrollment)
            db.session.commit()
            flash('Student enrolled successfully.', 'success')

    return render_template('user/enroll_student.html', form=form)



# TODO move it to admin under templates (this is the admin assigning units)
@main.route('/assign_unit', methods=['GET', 'POST'])
def assign_unit():
    form = AssignUnitForm()

    if form.validate_on_submit():
        lecturer_id = form.lecturer_id.data
        unit_id = form.unit_id.data
        academic_year = form.academic_year.data

        # Check if the unit is not already assigned to a lecturer
        assignment_exists = LecturerAssignment.query.filter_by(lecturer_id=lecturer_id,unit_id=unit_id, academic_year=academic_year).first()
        if assignment_exists:
            flash('Unit is already assigned to a lecturer.', 'warning')
            print("user exists")
        else:
            # Create a new assignment
            new_assignment = LecturerAssignment(lecturer_id=lecturer_id, unit_id=unit_id, academic_year=academic_year)
            db.session.add(new_assignment)
            db.session.commit()
            flash('Unit assigned to lecturer successfully.', 'success')

    return render_template('user/assign_unit.html', form=form)

# @main.route('/addmarks',methods=['GET','POST'])
# def addmarks():
#     if request.method == 'POST':
#         enrollment_id = request.form.get('enrollment_id')
#         # Retrieve other form data as needed

#         # Perform validation and save marks to the database
#         # Example: Create a new Marks object and add it to the database
#         new_marks = Marks(
#             enrollment_id=enrollment_id,
#             cat_marks=request.form.get('cat_marks'),
#             assignment_marks=request.form.get('assignment_marks'),
#             practical_marks=request.form.get('practical_marks'),
#             exam_marks=request.form.get('exam_marks'),
#             overall_marks=request.form.get('overall_marks'),
#             status=request.form.get('status')
#         )

#         db.session.add(new_marks)
#         db.session.commit()

#         flash('Marks submitted successfully.', 'success')
#         return redirect(url_for('main.addmarks'))

#     return render_template('user/addmarks.html')

# @main.route('/addmarks', methods=['GET', 'POST'])
# @login_required
# def addmarks():
#     if current_user.is_authenticated and current_user.role.name == 'Lecturer':
#         lecturer_id = current_user.id

#         # Fetch assigned units for the lecturer
#         assigned_units = (
#             LecturerAssignment.query
#             .filter_by(lecturer_id=lecturer_id)
#             .with_entities(LecturerAssignment.unit_id, LecturerAssignment.academic_year)
#             .all()
#         )

#         if assigned_units:
#             print("There exists permission for", current_user.username)
#             enrolled_students = []

#             # Fetch enrolled students for each assigned unit
#             for assigned_unit in assigned_units:
#                 academic_year = assigned_unit.academic_year
#                 unit_id = assigned_unit.unit_id

#                 students = (
#                     User.query
#                     .join(StudentEnrollment)
#                     .join(EnrollmentUnits)
#                     .join(Units)
#                     .add_columns(
#                         User.id.label('user_id'),
#                         User.fname,
#                         User.lname,
#                         User.email,
#                         Units.name.label('unit_name'),
#                         Units.code.label('unit_code'),
#                         EnrollmentUnits.id.label('enrollment_id')
#                     )
#                     .filter(
#                         Units.id == unit_id,
#                         StudentEnrollment.academic_year == academic_year
#                     )
#                     .all()
#                 )

#                 enrolled_students.extend(students)

#             # Create a list of dictionaries to hold student data
#             student_data = [
#                 {
#                     'user_id': student.user_id,
#                     'fname': student.fname,
#                     'lname': student.lname,
#                     'email': student.email,
#                     'unit_name': student.unit_name,
#                     'unit_code': student.unit_code,
#                     'enrollment_id':student.enrollment_id
#                 }
#                 for student in enrolled_students
#             ]

#             form = MarksInputForm()

#             if form.validate_on_submit():
#                 # Process the form data and add marks to the database
#                 for student in enrolled_students:
#                     # Assuming you have a Marks model
#                     marks = Marks(
#                         enrollment_id=form.enrollment_id,  # Replace with the actual enrollment_id for the student
#                         cat_marks=form.cat_marks.data,
#                         assignment_marks=form.assignment_marks.data,
#                         practical_marks=form.practical_marks.data,
#                         exam_marks=form.exam_marks.data,
#                         overall_marks=calculate_overall_marks(
#                             form.cat_marks.data,
#                             form.assignment_marks.data,
#                             form.practical_marks.data,
#                             form.exam_marks.data
#                         ),
#                         status=calculate_status(
#                             calculate_overall_marks(
#                                 form.cat_marks.data,
#                                 form.assignment_marks.data,
#                                 form.practical_marks.data,
#                                 form.exam_marks.data
#                             )
#                         )
#                     )

#                     db.session.add(marks)
#                     db.session.commit()

#                 flash('Marks added successfully!', 'success')
#                 return redirect(url_for('dashboard'))  # Redirect to your dashboard route after adding marks

#             return render_template('add_marks.html', student_data=student_data, form=form)

#     return redirect(url_for('user.login'))  # Redirect to login if not authenticated or not a lecturer



# lecture adding marks
@main.route('/addmarks', methods=['GET', 'POST'])
@login_required
def addmarks():
    if current_user.is_authenticated and current_user.role.name == 'Lecturer':
        lecturer_id = current_user.id

        # Fetch assigned units for the lecturer
        assigned_units = (
            LecturerAssignment.query
            .filter_by(lecturer_id=lecturer_id)
            .with_entities(LecturerAssignment.unit_id, LecturerAssignment.academic_year)
            .all()
        )

        if assigned_units:
            enrolled_students = []

            # Fetch enrolled students for each assigned unit
            for assigned_unit in assigned_units:
                academic_year = assigned_unit.academic_year
                unit_id = assigned_unit.unit_id

                students = (
                    User.query
                    .join(StudentEnrollment)
                    .join(EnrollmentUnits)
                    .join(Units)
                    .add_columns(
                        User.id.label('user_id'),
                        User.fname,
                        User.lname,
                        User.email,
                        Units.name.label('unit_name'),
                        Units.code.label('unit_code'),
                        EnrollmentUnits.id.label('enrollment_id')
                    )
                    .filter(
                        Units.id == unit_id,
                        StudentEnrollment.academic_year == academic_year
                    )
                    .all()
                )

                enrolled_students.extend(students)

            # Handle form submission
            form = AddMarksForm()
            if form.validate_on_submit():
                # Process the submitted form data here (e.g., update the database with the entered marks)
                flash('Marks added successfully!', 'success')
                return redirect(url_for('main.addmarks'))

            return render_template('addmarks.html', students=enrolled_students, form=form)

    # Handle the case where the user is not a lecturer
    flash('Permission denied. You must be a lecturer to access this page.', 'danger')
    return redirect(url_for('main.index'))
def calculate_status(cat_marks, assignment_marks, practical_marks, exam_marks):
    # Customize this logic based on your grading system
    total_marks = cat_marks + assignment_marks + practical_marks + exam_marks

    if total_marks >= 70:
        return 'Distinction'
    elif 60 <= total_marks < 70:
        return 'Credit'
    elif 50 <= total_marks < 60:
        return 'Pass'
    else:
        return 'Fail'

def calculate_overall_marks(cat_marks, assignment_marks, practical_marks, exam_marks):
    # Customize this logic based on your weighting system
    overall_marks = (cat_marks * 0.2) + (assignment_marks * 0.3) + (practical_marks * 0.2) + (exam_marks * 0.3)
    return overall_marks
