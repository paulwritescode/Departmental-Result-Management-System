from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)

from .. import db
from ..decorators import admin_required, permission_required
from ..models import (EnrollmentUnits, LecturerAssignment, Marks, Modules,
                      Permission, StudentEnrollment, Units, User)
from . import main
from .forms import *


@main.route('/',methods=['GET','POST','PUT'])
@login_required
@permission_required(Permission.VIEW)
def home():
  if current_user.is_authenticated and current_user.role.name == 'Lecturer':
    lecturer_id = current_user.id

    if request.method=='GET':

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

                    User.fname.label('student_fname'),
                    User.lname.label("student_lname"),
                    User.Reg_no.label("student_regNo"),
                    Units.name.label("unit_name"),
                    Units.code.label("unit_code"),
                    EnrollmentUnits.id.label("unitenrollment_id"),
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
            for student_fname,student_lname,student_regNo,unit_name,unit_code,unitenrollment_id,academicYear in students:
                 InMyUnit.append({
                    "enrollment_id":unitenrollment_id,
                    "student_name": student_fname + student_lname,
                    "course_name": unit_name,
                    "course_code": unit_code,
                    "student_reg": student_regNo,
                    "academicYear":academicYear
                             })
            return render_template('user/add_marks.html',students=InMyUnit)
    elif request.method=='POST':
        print("Currently in post Method 😂🥳🥳")
        enrollment_id=request.form.getlist('enrollment_id[]')
        catmarks=request.form.getlist('cat_marks[]')
        assignmentmarks=request.form.getlist('assignment_marks[]')
        practicalmarks=request.form.getlist('practical_marks[]')
        exammarks=request.form.getlist('exam_marks[]')

        print(enrollment_id)
        print(catmarks)
        print(assignmentmarks)
        print(practicalmarks)
        print(exammarks)
        for enrollment_id,catmarks,assignmentmarks,practicalmarks,exammarks in zip(enrollment_id,catmarks,assignmentmarks,practicalmarks,exammarks):
            overallmarks = 0.2 * float(catmarks) + 0.1 * float(assignmentmarks) + 0.1 * float(practicalmarks) + 0.6 * float(exammarks)


            new_mark=Marks(enrollment_id=enrollment_id,cat_marks=catmarks,assignment_marks=assignmentmarks,practical_marks=practicalmarks,exam_marks=exammarks,overall_marks=overallmarks,status=1)
            db.session.add(new_mark)
        db.session.commit()

        return("added Successfully")
    elif request.method == 'PUT':
    # Fetch all data from the Marks table
        all_marks_data = Marks.query.all()

    # Process data and create a dictionary for easier lookup
        marks_dict = {}
        for mark_data in all_marks_data:
            marks_dict[mark_data.enrollment_id] = {
            'cat_marks': mark_data.cat_marks,
            'assignment_marks': mark_data.assignment_marks,
            'practical_marks': mark_data.practical_marks,
            'exam_marks': mark_data.exam_marks,
            'overall_marks': mark_data.overall_marks,
            'status': mark_data.status,
        }

    # Fetch existing data where marks are null
        null_marks_data = Marks.query.filter(Marks.overall_marks.is_(None)).all()

    # Create a list to store data for rendering in the template
        marks_for_template = []

        for null_mark_data in null_marks_data:
            enrollment_id = null_mark_data.enrollment_id

        # Check if data exists in the marks_dict
            if enrollment_id in marks_dict:
                 marks_data = marks_dict[enrollment_id]
            else:
            # If data doesn't exist, create empty data
                marks_data = {
                    'cat_marks': '',
                    'assignment_marks': '',
                    'practical_marks': '',
                    'exam_marks': '',
                    'overall_marks': '',
                    'status': '',
                }

        marks_for_template.append({
            'enrollment_id': enrollment_id,
            'cat_marks': marks_data['cat_marks'],
            'assignment_marks': marks_data['assignment_marks'],
            'practical_marks': marks_data['practical_marks'],
            'exam_marks': marks_data['exam_marks'],
            'overall_marks': marks_data['overall_marks'],
            'status': marks_data['status'],
        })

        return render_template('user/update_marks.html', marks=marks_for_template)
    return render_template("user/user-base.html" ,title = 'Lecture Landing page ' )


@main.route("/editprofile",methods=['GET','PUT','POST'])
@login_required
def editprofile():
     if current_user.is_authenticated:
        user_id = current_user.id
        if request.method=='GET':
            user_profile = (
                User.query
                    .filter_by(id=user_id)
                    .with_entities(User.fname, User.lname, User.email, User.phone, User.current_module, User.Reg_no, User.role_id, User.status, User.Year_of_Registration, User.username)
                        .first()
                            )

    # Check if the user profile is found
            if user_profile:
                 fname, lname, email, phone, currentmodule, regno, roleid, status, yor, username = user_profile

                 return render_template('user/edit_profile.html', 
                               fname=fname,
                               lname=lname,
                               email=email,
                               phone=phone,
                               currentmodule=currentmodule,
                               regno=regno,
                               roleid=roleid,
                               status=status,
                               yor=yor,
                               username=username,
                               uid=user_id
                               )
            else:
        # Handle the case where the user profile is not found
                  return render_template('error.html', message='User profile not found')
        elif request.method=='POST':
            user=User.query.filter_by(id=user_id).all()
            if user:
                fname=request.form.get('fname')
                lname=request.form.get('lname')
                email=request.form.get('email')
                phone=request.form.get('phone')
                currentmodule=request.form.get('currentmodule')
                regno=request.form.get('regno')
                roleid=request.form.get('roleid')
                status=request.form.get('status')
                yor=request.form.get('yor')
                username=request.form.get('username')
                uid=request.form.get('uid')
                print(fname, lname, email, phone, currentmodule, regno, roleid, status, yor, username,uid)
                new_data = {
                    'fname': fname,
                    'lname': lname,
                    'email': email,
                    'phone': phone,
                    'current_module': currentmodule,
                    'Reg_no': regno,
                    'role_id':roleid,  # Replace with the new role id
                    'status': status,
                    'Year_of_Registration': yor,  # Replace with the new year of registration
                    'username': username
}
                db.session.query(User).filter_by(id=user_id).update(new_data)

            db.session.commit()

# Use the update method to update the user profile

            
            return("success")
     else:
         return ('User profile not found')



@main.route("/profile",methods=['GET'])
@login_required
def profile():
        if current_user.is_authenticated:
            user_id = current_user.id
            if request.method=='GET':
                user_profile = (
                User.query
                    .filter_by(id=user_id)
                    .with_entities(User.fname, User.lname, User.email, User.phone, User.current_module, User.Reg_no, User.role_id, User.status, User.Year_of_Registration, User.username)
                        .first()
                            )

    # Check if the user profile is found
                if user_profile:
                 fname, lname, email, phone, currentmodule, regno, roleid, status, yor, username = user_profile

                 return render_template('user/viewprofile.html', 
                               fname=fname,
                               lname=lname,
                               email=email,
                               phone=phone,
                               currentmodule=currentmodule,
                               regno=regno,
                               roleid=roleid,
                               status=status,
                               yor=yor,
                               username=username,
                               uid=user_id
                               )
            else:
                  return redirect(url_for("main.home"))
        # Handle the case where the user profile is not found
        else:    
            return ('User profile not found')
       


        
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
          
            
            for unit in enroll_units:
                new_unit_enrollment=EnrollmentUnits(enrollment_id=new_enrollment_id,unit_id=unit.id)
                print(new_unit_enrollment)
                db.session.add(new_unit_enrollment)
                db.session.commit()
                newmarkenrollmentid=new_unit_enrollment.id
                print(newmarkenrollmentid)
                new_unit_mark=(Marks(enrollment_id=new_unit_enrollment.id))
                db.session.add(new_unit_mark)
                print(new_enrollment_id)
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
@main.route('/update_marks', methods=['POST','GET','PUT'])
def update_marks():
    if current_user.is_authenticated and current_user.role.name == 'Lecturer':
        lecturer_id = current_user.id
    # Ensure the request is a POST request
        if request.method == 'PUT':
            print('post received')
            # Get data from the form
            enrollment_ids = request.form.getlist('enrollment_id[]')
            cat_marks = request.form.getlist('cat_marks[]')
            assignment_marks = request.form.getlist('assignment_marks[]')
            practical_marks = request.form.getlist('practical_marks[]')
            exam_marks = request.form.getlist('exam_marks[]')

            print(enrollment_id,cat_marks,assignment_marks)

            # Loop through the data and update marks
            for enrollment_id, cat_mark, assignment_mark, practical_mark, exam_mark in zip(
                    enrollment_ids, cat_marks, assignment_marks, practical_marks, exam_marks):

                # Retrieve the existing mark record for the student
                existing_mark = Marks.query.filter_by(enrollment_id=enrollment_id).first()

                # Check if the mark record exists
                if existing_mark:
                    # Update the marks if they are null
                    if existing_mark.cat_marks is None:
                        existing_mark.cat_marks = float(cat_mark)
                    if existing_mark.assignment_marks is None:
                        existing_mark.assignment_marks = float(assignment_mark)
                    if existing_mark.practical_marks is None:
                        existing_mark.practical_marks = float(practical_mark)
                    if existing_mark.exam_marks is None:
                        existing_mark.exam_marks = float(exam_mark)

                    # Calculate overall marks
                    overall_marks = (
                            0.2 * float(existing_mark.cat_marks) +
                            0.1 * float(existing_mark.assignment_marks) +
                            0.1 * float(existing_mark.practical_marks) +
                            0.6 * float(existing_mark.exam_marks)
                    )

                    existing_mark.overall_marks = overall_marks
                    print(existing_mark,)

                    # Commit the changes to the database
                    db.session.commit()

            # Redirect to the home page or another appropriate page
            return redirect(url_for('main.home'))
        

        elif request.method=='GET':

            marrks=db.session.query(
                Marks,
                User.fname.label("studentfname"),
                User.lname.label("studentlname"),
                User.Reg_no.label("stdentreg"),
                Units.code.label("unitcode"),
                Units.name.label("unitname"),
                StudentEnrollment.id.label("SUid"),
                EnrollmentUnits.id.label("EUid"), 
                Marks.id.label("markid")
            ).join(EnrollmentUnits,Marks.enrollment_id==EnrollmentUnits.id
                   ).join(StudentEnrollment,EnrollmentUnits.enrollment_id==StudentEnrollment.id
                          ).join(Units,EnrollmentUnits.unit_id==Units.id
                                 ).join(User,StudentEnrollment.student_id==User.id)
            
                          
        # Now you can use the lecturer_id in your queries or any other logic
        # For example, querying for units assigned to the lecturer
            assigned_units = (
                LecturerAssignment.query
                .filter_by(lecturer_id=lecturer_id)
                .with_entities(LecturerAssignment.unit_id, LecturerAssignment.academic_year)
                .all()
            )

            if assigned_units:
                
                enrolled_students = []
                for assigned_unit in assigned_units:
                    academic_year = assigned_unit.academic_year
                    unit_id = assigned_unit.unit_id
                    markis=marrks.filter(User.id==2)
                    makrs=markis.all()
                    
                    query=db.session.query(

                        User.fname.label('student_fname'),
                        User.lname.label("student_lname"),
                        User.Reg_no.label("student_regNo"),
                        Units.name.label("unit_name"),
                        Units.code.label("unit_code"),
                         Marks.id.label("mark_id"),
                        Marks.cat_marks.label("cats"),
                        Marks.assignment_marks.label("assignments"),
                        Marks.practical_marks.label("practicals"),
                        Marks.exam_marks.label("exam"),
                        Marks.overall_marks.label("overall"),
                       


                        EnrollmentUnits.id.label("unitenrollment_id"),
                        StudentEnrollment.academic_year.label("academicYear")
                        ).join(
                            StudentEnrollment,EnrollmentUnits.enrollment_id==StudentEnrollment.id
                        ).join(
                            User,StudentEnrollment.student_id==User.id
                        ).join(
                            Units, EnrollmentUnits.unit_id==Units.id
                        ).join(Marks,EnrollmentUnits.id==Marks.enrollment_id
                        )
                    enrolledStudents=query.filter(Units.id == unit_id,
                        StudentEnrollment.academic_year == academic_year)
                students=enrolledStudents.all()
                InMyUnit=[]
             
                 
                for student_fname,student_lname,student_regNo,unit_name,unit_code,mark_id ,cats,assignments,practicals,exam,overall,unitenrollment_id,academicYear in students:
                    InMyUnit.append({
                       
                        "student_name": student_fname + student_lname,
                        "course_name": unit_name,
                        "course_code": unit_code,
                        "enrollment_id":unitenrollment_id,
                        "student_reg": student_regNo,
                        "academicYear":academicYear,
                        "cats":cats,
                        "assignments":assignments,
                        "practicals":practicals,
                        "exams":exam,
                        "overall":overall,
                        "markid":mark_id,
                                })
               
                    
                return render_template('user/update_marks.html',students=InMyUnit)
       
        elif request.method == 'POST':
          
            enrollment_id=request.form.getlist('enrollment_id[]')
            catmarks=request.form.getlist('cat_marks[]')
            assignmentmarks=request.form.getlist('assignment_marks[]')
            practicalmarks=request.form.getlist('practical_marks[]')
            exammarks=request.form.getlist('exam_marks[]')
            mark_id=request.form.getlist('mark_id[]')

           
            for enrollment_id,catmarks,assignmentmarks,practicalmarks,exammarks,mark_id in zip(enrollment_id,catmarks,assignmentmarks,practicalmarks,   exammarks,mark_id):
        
             mark_record = Marks.query.filter_by(id=mark_id).first()
            #  mark_record.change_status()
           
             
             if mark_record:
                catMarks=  mark_record.cat_marks
                if catMarks is  None or catMarks=="":
                    mark_record.cat_marks = float(catmarks) if catmarks else None
                assignmentsMarks=mark_record.assignment_marks
                if assignmentsMarks is None or assignmentsMarks=="":
                    mark_record.assignment_marks = float(assignmentmarks) if assignmentmarks else None
                practicalMarks=mark_record.practical_marks
                if practicalMarks is  None or practicalMarks=="":
                    mark_record.practical_marks = float(practicalmarks) if practicalmarks else None
                examMarks=mark_record.exam_marks
             
                
             
                status=mark_record.status
                if exammarks and examMarks is  None or exammarks and examMarks!=exammarks or exammarks and examMarks=="":
                    mark_record.exam_marks = float(exammarks) if exammarks else None
                if (exammarks is not None and examMarks is None and exammarks!="" and examMarks!=exammarks)or (examMarks!="" and exammarks is not None and exammarks!="" and examMarks!=exammarks ):
                 
                    catmarks=float(catmarks) if catmarks else  0
                    assignmentmarks=float(assignmentmarks) if assignmentmarks else 0
                    practicalmarks=float(practicalmarks)if practicalmarks else 0
                    exammark=float(exammarks)
                    ov_all=(0.66*catmarks)+(assignmentmarks)+(0.5*practicalmarks)+(exammark)
                    mark_record.overall_marks=float(ov_all)
                    input=float(exammarks)
                    record=float(examMarks)
                    if ov_all > 39:
                        Marks.query.filter_by(id=mark_id).update({Marks.status:1})
                    elif ov_all<40 and record!=input:
                        Marks.query.filter_by(id=mark_id).update({Marks.status: Marks.status + 2})




              
             db.session.commit()



            return redirect(url_for('main.update_marks'))
        
        else:
            return jsonify({Invalid method }), 404
    
    return redirect(url_for('main.home'))