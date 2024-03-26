from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from sqlalchemy import and_

from .. import db
from ..decorators import admin_required, permission_required
from ..models import (
    EnrollmentUnits,
    LecturerAssignment,
    Marks,
    Modules,
    Permission,
    StudentEnrollment,
    Units,
    User,
)
from . import main
from .forms import *


@main.route("/", methods=["GET", "POST", "PUT"])
@login_required
@permission_required(Permission.VIEW)
def home():

    return render_template("user/index.html")
    if current_user.is_authenticated and current_user.role.name == "Lecturer":
        lecturer_id = current_user.id

        if request.method == "GET":

            # Now you can use the lecturer_id in your queries or any other logic
            # For example, querying for units assigned to the lecturer
            assigned_units = (
                db.session.query(
                    LecturerAssignment.unit_id,
                    LecturerAssignment.academic_year,
                    Units.name,
                )
                .join(Units, Units.id == LecturerAssignment.unit_id)
                .filter(LecturerAssignment.lecturer_id == lecturer_id)
                .all()
            )

            lecturers_units = []
            for unit in assigned_units:
                print("There exists permission for", current_user.username)
                print(assigned_units)
                print(unit)

            return render_template(
                "user/lecturerlandingpage.html", lecturerunits=assigned_units
            )


def addmarksfirsttime():
    if current_user.is_authenticated and current_user.role.name == "Lecturer":
        lecturer_id = current_user.id

        if request.method == "GET":

            # Now you can use the lecturer_id in your queries or any other logic
            # For example, querying for units assigned to the lecturer
            assigned_units = (
                LecturerAssignment.query.filter_by(lecturer_id=lecturer_id)
                .with_entities(
                    LecturerAssignment.unit_id, LecturerAssignment.academic_year
                )
                .all()
            )

            if assigned_units:
                print("There exists permission for", current_user.username)
                enrolled_students = []
                for assigned_unit in assigned_units:
                    academic_year = assigned_unit.academic_year
                    unit_id = assigned_unit.unit_id
                    query = (
                        db.session.query(
                            User.fname.label("student_fname"),
                            User.lname.label("student_lname"),
                            User.Reg_no.label("student_regNo"),
                            Units.name.label("unit_name"),
                            Units.code.label("unit_code"),
                            EnrollmentUnits.id.label("unitenrollment_id"),
                            StudentEnrollment.academic_year.label("academicYear"),
                        )
                        .join(
                            StudentEnrollment,
                            EnrollmentUnits.enrollment_id == StudentEnrollment.id,
                        )
                        .join(User, StudentEnrollment.student_id == User.id)
                        .join(Units, EnrollmentUnits.unit_id == Units.id)
                    )
                    enrolledStudents = query.filter(
                        Units.id == unit_id,
                        StudentEnrollment.academic_year == academic_year,
                    )
                students = enrolledStudents.all()
                InMyUnit = []
                for student_data in students:
                    print(student_data)
                for (
                    student_fname,
                    student_lname,
                    student_regNo,
                    unit_name,
                    unit_code,
                    unitenrollment_id,
                    academicYear,
                ) in students:
                    InMyUnit.append(
                        {
                            "enrollment_id": unitenrollment_id,
                            "student_name": student_fname + student_lname,
                            "course_name": unit_name,
                            "course_code": unit_code,
                            "student_reg": student_regNo,
                            "academicYear": academicYear,
                        }
                    )
                return render_template("user/add_marks.html", students=InMyUnit)
        elif request.method == "POST":
            print("Currently in post Method 😂🥳🥳")
            enrollment_id = request.form.getlist("enrollment_id[]")
            catmarks = request.form.getlist("cat_marks[]")
            assignmentmarks = request.form.getlist("assignment_marks[]")
            practicalmarks = request.form.getlist("practical_marks[]")
            exammarks = request.form.getlist("exam_marks[]")

            print(enrollment_id)
            print(catmarks)
            print(assignmentmarks)
            print(practicalmarks)
            print(exammarks)
            for (
                enrollment_id,
                catmarks,
                assignmentmarks,
                practicalmarks,
                exammarks,
            ) in zip(
                enrollment_id, catmarks, assignmentmarks, practicalmarks, exammarks
            ):
                overallmarks = (
                    0.2 * float(catmarks)
                    + 0.1 * float(assignmentmarks)
                    + 0.1 * float(practicalmarks)
                    + 0.6 * float(exammarks)
                )

                new_mark = Marks(
                    enrollment_id=enrollment_id,
                    cat_marks=catmarks,
                    assignment_marks=assignmentmarks,
                    practical_marks=practicalmarks,
                    exam_marks=exammarks,
                    overall_marks=overallmarks,
                    status=1,
                )
                db.session.add(new_mark)
            db.session.commit()

            return "added Successfully"
        elif request.method == "PUT":
            # Fetch all data from the Marks table
            all_marks_data = Marks.query.all()

            # Process data and create a dictionary for easier lookup
            marks_dict = {}
            for mark_data in all_marks_data:
                marks_dict[mark_data.enrollment_id] = {
                    "cat_marks": mark_data.cat_marks,
                    "assignment_marks": mark_data.assignment_marks,
                    "practical_marks": mark_data.practical_marks,
                    "exam_marks": mark_data.exam_marks,
                    "overall_marks": mark_data.overall_marks,
                    "status": mark_data.status,
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
                        "cat_marks": "",
                        "assignment_marks": "",
                        "practical_marks": "",
                        "exam_marks": "",
                        "overall_marks": "",
                        "status": "",
                    }

            marks_for_template.append(
                {
                    "enrollment_id": enrollment_id,
                    "cat_marks": marks_data["cat_marks"],
                    "assignment_marks": marks_data["assignment_marks"],
                    "practical_marks": marks_data["practical_marks"],
                    "exam_marks": marks_data["exam_marks"],
                    "overall_marks": marks_data["overall_marks"],
                    "status": marks_data["status"],
                }
            )

            return render_template("user/update_marks.html", marks=marks_for_template)
        return render_template("user/user-base.html", title="Lecture Landing page ")


@main.route("/editprofile", methods=["GET", "PUT", "POST"])
@login_required
def editprofile():
    if current_user.is_authenticated:
        user_id = current_user.id
        if request.method == "GET":
            user_profile = (
                User.query.filter_by(id=user_id)
                .with_entities(
                    User.fname,
                    User.lname,
                    User.email,
                    User.phone,
                    User.current_module,
                    User.Reg_no,
                    User.role_id,
                    User.status,
                    User.Year_of_Registration,
                    User.username,
                )
                .first()
            )

            # Check if the user profile is found
            if user_profile:
                (
                    fname,
                    lname,
                    email,
                    phone,
                    currentmodule,
                    regno,
                    roleid,
                    status,
                    yor,
                    username,
                ) = user_profile

                return render_template(
                    "user/edit_profile.html",
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
                    uid=user_id,
                )
            else:
                # Handle the case where the user profile is not found
                return render_template("error.html", message="User profile not found")
        elif request.method == "POST":
            user = User.query.filter_by(id=user_id).all()
            if user:
                fname = request.form.get("fname")
                lname = request.form.get("lname")
                email = request.form.get("email")
                phone = request.form.get("phone")
                currentmodule = request.form.get("currentmodule")
                regno = request.form.get("regno")
                roleid = request.form.get("roleid")
                status = request.form.get("status")
                yor = request.form.get("yor")
                username = request.form.get("username")
                uid = request.form.get("uid")
                print(
                    fname,
                    lname,
                    email,
                    phone,
                    currentmodule,
                    regno,
                    roleid,
                    status,
                    yor,
                    username,
                    uid,
                )
                new_data = {
                    "fname": fname,
                    "lname": lname,
                    "email": email,
                    "phone": phone,
                    "current_module": currentmodule,
                    "Reg_no": regno,
                    "role_id": roleid,  # Replace with the new role id
                    "status": status,
                    "Year_of_Registration": yor,  # Replace with the new year of registration
                    "username": username,
                }
                db.session.query(User).filter_by(id=user_id).update(new_data)

            db.session.commit()

            # Use the update method to update the user profile

            return "success"
    else:
        return "User profile not found"


@main.route("/profile", methods=["GET"])
@login_required
def profile():
    if current_user.is_authenticated:
        user_id = current_user.id
        if request.method == "GET":
            user_profile = (
                User.query.filter_by(id=user_id)
                .with_entities(
                    User.fname,
                    User.lname,
                    User.email,
                    User.phone,
                    User.current_module,
                    User.Reg_no,
                    User.role_id,
                    User.status,
                    User.Year_of_Registration,
                    User.username,
                )
                .first()
            )

            # Check if the user profile is found
            if user_profile:
                (
                    fname,
                    lname,
                    email,
                    phone,
                    currentmodule,
                    regno,
                    roleid,
                    status,
                    yor,
                    username,
                ) = user_profile

                return render_template(
                    "user/viewprofile.html",
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
                    uid=user_id,
                )
        else:
            return redirect(url_for("main.home"))
    # Handle the case where the user profile is not found
    else:
        return "User profile not found"


# lecture adding marks
@main.route("/addmarks", methods=["GET", "POST"])
@login_required
def addmarks():
    if current_user.is_authenticated and current_user.role.name == "Lecturer":
        lecturer_id = current_user.id

        # Fetch assigned units for the lecturer
        assigned_units = (
            LecturerAssignment.query.filter_by(lecturer_id=lecturer_id)
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
                    User.query.join(StudentEnrollment)
                    .join(EnrollmentUnits)
                    .join(Units)
                    .add_columns(
                        User.id.label("user_id"),
                        User.fname,
                        User.lname,
                        User.email,
                        Units.name.label("unit_name"),
                        Units.code.label("unit_code"),
                        EnrollmentUnits.id.label("enrollment_id"),
                    )
                    .filter(
                        Units.id == unit_id,
                        StudentEnrollment.academic_year == academic_year,
                    )
                    .all()
                )

                enrolled_students.extend(students)

            # Handle form submission
            form = AddMarksForm()
            if form.validate_on_submit():
                # Process the submitted form data here (e.g., update the database with the entered marks)
                flash("Marks added successfully!", "success")
                return redirect(url_for("main.addmarks"))

            return render_template(
                "addmarks.html", students=enrolled_students, form=form
            )

    # Handle the case where the user is not a lecturer
    flash("Permission denied. You must be a lecturer to access this page.", "danger")
    return redirect(url_for("main.index"))


def calculate_status(cat_marks, assignment_marks, practical_marks, exam_marks):
    # Customize this logic based on your grading system
    total_marks = cat_marks + assignment_marks + practical_marks + exam_marks

    if total_marks >= 70:
        return "Distinction"
    elif 60 <= total_marks < 70:
        return "Credit"
    elif 50 <= total_marks < 60:
        return "Pass"
    else:
        return "Fail"


def calculate_overall_marks(cat_marks, assignment_marks, practical_marks, exam_marks):
    # Customize this logic based on your weighting system
    overall_marks = (
        (cat_marks * 0.2)
        + (assignment_marks * 0.3)
        + (practical_marks * 0.2)
        + (exam_marks * 0.3)
    )
    return overall_marks


@main.route("/test", methods=["GET"])
def test():
    query = (
        db.session.query(
            User.fname.label("fname"),
            User.lname.label("lname"),
            User.Reg_no.label("reg"),
            Modules.year.label("year"),
            Modules.semester.label("sem"),
            Units.name.label("unit_name"),
            Units.code.label("unit_code"),
            Marks.overall_marks.label("overall"),
            EnrollmentUnits.id.label("unitenrollment_id"),
            StudentEnrollment.academic_year.label("academicYear"),
        )
        .join(StudentEnrollment, EnrollmentUnits.enrollment_id == StudentEnrollment.id)
        .join(User, StudentEnrollment.student_id == User.id)
        .join(Units, EnrollmentUnits.unit_id == Units.id)
        .join(Marks, EnrollmentUnits.id == Marks.unitenrollment_id)
    )
    enrolledStudents = query.filter(
        StudentEnrollment.module_id == 2,
        StudentEnrollment.academic_year == 20222023,
        User.Reg_no == 1255,
    ).group_by(Units.name)
    students = enrolledStudents.all()

    print(f"query returns {students} while list inyear")
    return "OLLA"


@main.route(
    "/getmarks/<int:student_id>/<string:academic_year>/<int:module_id>",
    methods=["GET", "POST"],
)
def getmarks(student_id, academic_year, module_id):
    results = (
        db.session.query(
            User.fname.label("fname"),
            User.lname.label("lname"),
            User.Reg_no.label("reg"),
            StudentEnrollment.id.label("studid"),
            Units.name.label("unitname"),
            Units.code.label("unitcode"),
            Marks.cat_marks.label("cats"),
            Marks.assignment_marks.label("assignments"),
            Marks.practical_marks.label("practicals"),
            Marks.exam_marks.label("exam"),
            Marks.overall_marks.label("unitmark"),
            Marks.status.label("markstatus"),
        )
        .join(EnrollmentUnits, Marks.unitenrollment_id == EnrollmentUnits.id)
        .join(StudentEnrollment, EnrollmentUnits.enrollment_id == StudentEnrollment.id)
        .join(Modules, StudentEnrollment.module_id == Modules.id)
        .join(User, StudentEnrollment.student_id == User.id)
        .join(Units, EnrollmentUnits.unit_id == Units.id)
        .filter(
            and_(
                StudentEnrollment.student_id == student_id,
                StudentEnrollment.academic_year == academic_year,
                StudentEnrollment.module_id == module_id,
            )
        )
        .all()
    )
    length = len(results)

    print(
        "criteria", "id", student_id, "academicyear", academic_year, "module", module_id
    )
    print(results)

    return render_template("user/Studentmarks.html", data=results, length=length)


@main.route("/results/<int:student_id>/<string:academic_year>", methods=["GET"])
def get_student_results(student_id, academic_year):
    results = (
        db.session.query(
            User.fname.label("fname"),
            User.lname.label("lname"),
            User.Reg_no.label("reg"),
            StudentEnrollment.id.label("studid"),
            Units.name.label("unitname"),
            Units.code.label("unitcode"),
            Marks.overall_marks.label("unitmark"),
        )
        .join(EnrollmentUnits, Marks.unitenrollment_id == EnrollmentUnits.id)
        .join(StudentEnrollment, EnrollmentUnits.enrollment_id == StudentEnrollment.id)
        .join(User, StudentEnrollment.student_id == User.id)
        .join(Units, EnrollmentUnits.unit_id == Units.id)
        .filter(
            and_(
                StudentEnrollment.student_id == student_id,
                StudentEnrollment.academic_year == academic_year,
            )
        )
        .all()
    )
    length = len(results)
    meanscore = 0
    recommendation = ""

    for i in range(length):
        if results[i][6] < 40:
            recommendation = "Fail"
        elif results[i][6] == 0:
            recommendation = "pending"
        meanscore = meanscore + results[i][6]
        print(meanscore)
    score = meanscore / length
    print(score)
    if score > 70 and recommendation is not "Fail" and recommendation is not "pending":
        Meangrade = "A"
        recommendation = "Excellent"
    elif (
        score > 59 and recommendation is not "Fail" and recommendation is not "pending"
    ):
        Meangrade = "B"
        recommendation = "Good"
    elif (
        score > 49 and recommendation is not "Fail" and recommendation is not "pending"
    ):
        Meangrade = "C"
        recommendation = "Satisfactory"
    elif (
        score > 39 and recommendation is not "Fail" and recommendation is not "pending"
    ):
        Meangrade = "D"

        recommendation = "Pass"
    elif score == 0:
        recommendation = "pending"
        Meangrade = "X"

    else:
        Meangrade = "E"
        recommendation = recommendation

    return render_template(
        "user/transcript.html",
        data=results,
        length=length,
        meangrade=Meangrade,
        recommendation=recommendation,
        meanscore=score,
    )


# Query to fetch all students enrolled in a certain academic year


@main.route("/studentYears")
def student_academic_year():
    print(current_user.role.name)
    if current_user.is_authenticated and current_user.role.name == "Student":
        student_id = current_user.id

        Years = (
            db.session.query(
                StudentEnrollment.academic_year.label("StudentYears"),
                StudentEnrollment.student_id.label("studid"),
                Modules.year.label("moduleyear"),
            )
            .join(Modules, StudentEnrollment.module_id == Modules.id)
            .filter(StudentEnrollment.student_id == student_id)
            .distinct()
            .all()
        )

        print(Years)
        return render_template("user/StudentYears.html", Years=Years)
    return ("unauthorized user", current_user.role.name)


@main.route("/modulemarks")
def student_modules():
    print(current_user.role.name)
    if current_user.is_authenticated and current_user.role.name == "Student":
        student_id = current_user.id

        Years = (
            db.session.query(
                StudentEnrollment.academic_year.label("StudentYears"),
                StudentEnrollment.student_id.label("studid"),
                Modules.year.label("moduleyear"),
                Modules.semester.label("module"),
                StudentEnrollment.module_id.label("moduleid"),
            )
            .join(Modules, StudentEnrollment.module_id == Modules.id)
            .filter(StudentEnrollment.student_id == student_id)
            .all()
        )

        print(Years)
        return render_template("user/StudentSemesters.html", Years=Years)
    return ("unauthorized user", current_user.role.name)
