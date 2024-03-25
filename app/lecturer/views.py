from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

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
from . import lecturer
from .forms import *


@lecturer.route("/lecturerdashboard", methods=["GET", "POST", "PUT"])
@login_required
@permission_required(Permission.VIEW)
def home():
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


@lecturer.route("/update_marks", methods=["POST", "GET", "PUT"])
def update_marks():
    acadyear = ""
    yunit = 0

    if current_user.is_authenticated and current_user.role.name == "Lecturer":
        lecturer_id = current_user.id
        # Ensure the request is a POST request
        if request.method == "PUT":
            print("post received")
            # Get data from the form
            enrollment_ids = request.form.getlist("enrollment_id[]")
            cat_marks = request.form.getlist("cat_marks[]")
            assignment_marks = request.form.getlist("assignment_marks[]")
            practical_marks = request.form.getlist("practical_marks[]")
            exam_marks = request.form.getlist("exam_marks[]")

            print(enrollment_id, cat_marks, assignment_marks)

            # Loop through the data and update marks
            for (
                enrollment_id,
                cat_mark,
                assignment_mark,
                practical_mark,
                exam_mark,
            ) in zip(
                enrollment_ids, cat_marks, assignment_marks, practical_marks, exam_marks
            ):

                # Retrieve the existing mark record for the student
                existing_mark = Marks.query.filter_by(
                    enrollment_id=enrollment_id
                ).first()

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
                        0.2 * float(existing_mark.cat_marks)
                        + 0.1 * float(existing_mark.assignment_marks)
                        + 0.1 * float(existing_mark.practical_marks)
                        + 0.6 * float(existing_mark.exam_marks)
                    )

                    existing_mark.overall_marks = overall_marks
                    print(
                        existing_mark,
                    )

                    # Commit the changes to the database
                    db.session.commit()

            # Redirect to the home page or another appropriate page
            return redirect(url_for("main.home"))

        elif request.method == "GET":
            acyear = request.args.get("acyear")
            unit = request.args.get("unit")
            print(acyear, unit)
            acadyear = acyear
            yunit = unit

            marrks = (
                db.session.query(
                    Marks,
                    User.fname.label("studentfname"),
                    User.lname.label("studentlname"),
                    User.Reg_no.label("stdentreg"),
                    Units.code.label("unitcode"),
                    Units.name.label("unitname"),
                    StudentEnrollment.id.label("SUid"),
                    EnrollmentUnits.id.label("EUid"),
                    Marks.id.label("markid"),
                )
                .join(EnrollmentUnits, Marks.unitenrollment_id == EnrollmentUnits.id)
                .join(
                    StudentEnrollment,
                    EnrollmentUnits.enrollment_id == StudentEnrollment.id,
                )
                .join(Units, EnrollmentUnits.unit_id == Units.id)
                .join(User, StudentEnrollment.student_id == User.id)
            )

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

                enrolled_students = []
                for assigned_unit in assigned_units:
                    academic_year = assigned_unit.academic_year
                    unit_id = assigned_unit.unit_id
                    markis = marrks.filter(User.id == 2)
                    makrs = markis.all()

                    query = (
                        db.session.query(
                            User.fname.label("student_fname"),
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
                            StudentEnrollment.academic_year.label("academicYear"),
                        )
                        .join(
                            StudentEnrollment,
                            EnrollmentUnits.enrollment_id == StudentEnrollment.id,
                        )
                        .join(User, StudentEnrollment.student_id == User.id)
                        .join(Units, EnrollmentUnits.unit_id == Units.id)
                        .join(Marks, EnrollmentUnits.id == Marks.unitenrollment_id)
                    )
                    enrolledStudents = query.filter(
                        Units.id == unit, StudentEnrollment.academic_year == acyear
                    )
                students = enrolledStudents.all()
                InMyUnit = []

                for (
                    student_fname,
                    student_lname,
                    student_regNo,
                    unit_name,
                    unit_code,
                    mark_id,
                    cats,
                    assignments,
                    practicals,
                    exam,
                    overall,
                    unitenrollment_id,
                    academicYear,
                ) in students:
                    InMyUnit.append(
                        {
                            "student_name": student_fname + student_lname,
                            "course_name": unit_name,
                            "course_code": unit_code,
                            "enrollment_id": unitenrollment_id,
                            "student_reg": student_regNo,
                            "academicYear": academicYear,
                            "cats": cats,
                            "assignments": assignments,
                            "practicals": practicals,
                            "exams": exam,
                            "overall": overall,
                            "markid": mark_id,
                        }
                    )

                return render_template("user/update_marks.html", students=InMyUnit)

        elif request.method == "POST":

            enrollment_id = request.form.getlist("enrollment_id[]")
            catmarks = request.form.getlist("cat_marks[]")
            assignmentmarks = request.form.getlist("assignment_marks[]")
            practicalmarks = request.form.getlist("practical_marks[]")
            exammarks = request.form.getlist("exam_marks[]")
            mark_id = request.form.getlist("mark_id[]")

            for (
                enrollment_id,
                catmarks,
                assignmentmarks,
                practicalmarks,
                exammarks,
                mark_id,
            ) in zip(
                enrollment_id,
                catmarks,
                assignmentmarks,
                practicalmarks,
                exammarks,
                mark_id,
            ):

                mark_record = Marks.query.filter_by(id=mark_id).first()
                #  mark_record.change_status()
                #  erkgbjhekgbjhrtkjhbt

                if mark_record:
                    catMarks = mark_record.cat_marks
                    if catMarks is None or catMarks == "":
                        mark_record.cat_marks = float(catmarks) if catmarks else None
                    assignmentsMarks = mark_record.assignment_marks
                    if assignmentsMarks is None or assignmentsMarks == "":
                        mark_record.assignment_marks = (
                            float(assignmentmarks) if assignmentmarks else None
                        )
                    practicalMarks = mark_record.practical_marks
                    if practicalMarks is None or practicalMarks == "":
                        mark_record.practical_marks = (
                            float(practicalmarks) if practicalmarks else None
                        )
                    examMarks = mark_record.exam_marks

                    status = mark_record.status
                    if (
                        exammarks
                        and examMarks is None
                        or exammarks
                        and examMarks != exammarks
                        or exammarks
                        and examMarks == ""
                    ):
                        mark_record.exam_marks = float(exammarks) if exammarks else None
                    if (
                        exammarks is not None
                        and examMarks is None
                        and exammarks != ""
                        and examMarks != exammarks
                    ) or (
                        examMarks != ""
                        and exammarks is not None
                        and exammarks != ""
                        and examMarks != exammarks
                    ):

                        catmarks = float(catmarks) if catmarks else 0
                        assignmentmarks = (
                            float(assignmentmarks) if assignmentmarks else 0
                        )
                        practicalmarks = float(practicalmarks) if practicalmarks else 0
                        exammark = float(exammarks)
                        ov_all = (
                            (0.66 * catmarks)
                            + (assignmentmarks)
                            + (0.5 * practicalmarks)
                            + (exammark)
                        )
                        mark_record.overall_marks = float(ov_all)
                        input = float(exammarks)
                        record = float(examMarks) if examMarks else 0
                        if (
                            catmarks == 0
                            or assignmentmarks == 0
                            or practicalmarks == 0
                            or exammark == 0
                        ):
                            Marks.query.filter_by(id=mark_id).update({Marks.status: -1})
                        elif (
                            ov_all > 39
                            and assignmentmarks is not None
                            and practicalmarks is not None
                            and catmarks is not None
                        ):
                            Marks.query.filter_by(id=mark_id).update({Marks.status: 1})
                        elif (
                            ov_all < 40
                            and record != input
                            and assignmentmarks is not None
                            and practicalmarks is not None
                            and catmarks is not None
                        ):
                            Marks.query.filter_by(id=mark_id).update(
                                {Marks.status: Marks.status + 2}
                            )

                db.session.commit()

            return redirect(url_for("lecturer.home"))

        else:
            return jsonify({"Invalid method"}), 404

    return redirect(url_for("main.home"))
