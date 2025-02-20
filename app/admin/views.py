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
from . import admin
from .forms import *


@admin.route("/enroll_student", methods=["GET", "POST"])
@admin_required
def enroll_student():
    form = EnrollStudentForm()
    if form.validate_on_submit():
        student_id = form.student_id.data
        module_id = form.module_id.data
        academic_year = form.academic_year.data

        # Check if the student is not already enrolled in the module
        enrollment_exists = StudentEnrollment.query.filter_by(
            student_id=student_id, module_id=module_id, academic_year=academic_year
        ).first()
        if enrollment_exists:
            flash("Student is already enrolled in the module.", "warning")
        else:
            # Create a new enrollment
            new_enrollment = StudentEnrollment(
                student_id=student_id, module_id=module_id, academic_year=academic_year
            )

            db.session.add(new_enrollment)
            db.session.commit()
            new_enrollment_id = new_enrollment.id
            enroll_units = Units.query.filter_by(module_id=module_id).all()

            for unit in enroll_units:
                new_unit_enrollment = EnrollmentUnits(
                    enrollment_id=new_enrollment_id, unit_id=unit.id
                )
                print(new_unit_enrollment)
                db.session.add(new_unit_enrollment)
                db.session.commit()
                newmarkenrollmentid = new_unit_enrollment.id
                print(newmarkenrollmentid)
                new_unit_mark = Marks(unitenrollment_id=new_unit_enrollment.id)
                db.session.add(new_unit_mark)
                print(new_enrollment_id)
            db.session.commit()
            flash("Student enrolled successfully.", "success")

    return render_template(
        "admin/enroll_student.html", form=form, title="Enroll Students"
    )


@admin.route("/assign_unit", methods=["GET", "POST"])
@admin_required
def assign_unit():
    form = AssignUnitForm()

    if form.validate_on_submit():
        lecturer_id = form.lecturer_id.data
        unit_id = form.unit_id.data
        academic_year = form.academic_year.data

        # Check if the unit is not already assigned to a lecturer
        assignment_exists = LecturerAssignment.query.filter_by(
            lecturer_id=lecturer_id, unit_id=unit_id, academic_year=academic_year
        ).first()
        if assignment_exists:
            flash("Unit is already assigned to a lecturer.", "warning")
            print("user exists")
        else:
            # Create a new assignment
            new_assignment = LecturerAssignment(
                lecturer_id=lecturer_id, unit_id=unit_id, academic_year=academic_year
            )
            db.session.add(new_assignment)
            db.session.commit()
            flash("Unit assigned to lecturer successfully.", "success")

    return render_template("admin/assign_unit.html", form=form, title="Assign Units")


@admin.route(
    "/consolidated_stylesheet/<string:acyear>/<int:yos>/<string:type>",
    methods=["POST", "GET"],
)
@permission_required(Permission.ADMIN)
@admin_required
def consosheet(acyear, yos, type):
    if request.method == "GET":

        query1 = (
            db.session.query(
                User.fname.label("userfname"),
                User.lname.label("userlname"),
                User.Reg_no.label("regno"),
                StudentEnrollment.student_id.label("StudentId"),
                Modules.year.label("modyear"),
                Modules.semester.label("modsem"),
                StudentEnrollment.id.label("seid"),
                StudentEnrollment.academic_year.label("academiyear"),
                StudentEnrollment.module_id.label("modid"),
                StudentEnrollment.student_id.label("studedid"),
            )
            .join(StudentEnrollment, User.id == StudentEnrollment.student_id)
            .join(Modules, StudentEnrollment.module_id == Modules.id)
        )
        enrolledStuents = query1.filter(
            StudentEnrollment.academic_year == acyear, Modules.year == yos
        )
        student = enrolledStuents.all()

        tester = []

        def func2(regno):

            result = []

            for (
                unit_name,
                unit_code,
                unit_id,
                overall,
                markstatus,
                uniten,
                acayea,
                reg,
            ) in students:
                if reg == regno:
                    result.append(
                        {
                            "unit": unit_name,
                            "unit_mark": overall,
                            "unit_id": unit_id,
                            "markstatus": markstatus,
                        }
                    )
            return result

        def func1():

            result = []

            for (
                unit_name,
                unit_code,
                unit_id,
                overall,
                markstatus,
                uniten,
                acayea,
                reg,
            ) in studentes:

                result.append(
                    {
                        "unit": unit_name,
                        "unit_mark": overall,
                        "unit_id": unit_id,
                        "markstatus": markstatus,
                    }
                )
            return result

        student_data_dict = []
        test = []
        for (
            fname,
            lname,
            regno,
            studid,
            modyear,
            modsem,
            seid,
            academiyear,
            modid,
            studedid,
        ) in student:
            query = (
                db.session.query(
                    Units.name.label("unit_name"),
                    Units.code.label("unit_code"),
                    Units.id.label("unit_id"),
                    Marks.overall_marks.label("overall"),
                    Marks.status.label("markstatus"),
                    EnrollmentUnits.id.label("unitenrollment_id"),
                    StudentEnrollment.academic_year.label("academicYear"),
                    User.Reg_no.label("regno"),
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
                EnrollmentUnits.enrollment_id == seid,
                StudentEnrollment.academic_year == acyear,
            )
            enrolledStudentes = query.filter(
                StudentEnrollment.id == studid,
                StudentEnrollment.academic_year == acyear,
            )
            students = enrolledStudents.all()
            studentes = enrolledStudentes.all()

            found = False

            for stud in student_data_dict:

                if regno == stud["reg"]:
                    if "module1" not in stud:
                        stud["module1"] = f"{modyear}.{modsem}"

                    elif "module1" in stud:
                        stud["module2"] = f"{modyear}.{modsem}"

                        stud["valuesmod2"] = func2(regno)
                        test.append(
                            {
                                "names" "module :" f"{modyear}.{modsem}",
                                "values :" f"{func2(regno)}",
                            }
                        )

                    found = True
                    break

            if not found:
                student_data_dict.append(
                    {
                        "names": fname + " " + lname,
                        "reg": regno,
                        "student_id": studedid,
                        "module1": f"{modyear}.{modsem}",
                        "values": func2(regno),
                    }
                )

            tester.append(
                {
                    "names": fname + " " + lname,
                    "reg": regno,
                    "student_id": studedid,
                    "module": f"{modyear}.{modsem}",
                    "values": func2(regno),
                }
            )

        for student_data in student_data_dict:
            total_marks = 0
            num_units = 0
            failed_units = 0
            Passlist = []
            Suppllementarylist = []
            Repeatyearlist = []
            Discontinuationlist = []

            status = "pass"  # Assume pass, change to fail if any unit fails
            for unit_data in student_data["values"] + student_data["valuesmod2"]:

                total_marks += unit_data["unit_mark"]
                num_units += 1

                if unit_data["markstatus"] != None:
                    if int(unit_data["markstatus"]) == 2:
                        status = "fail"
                        failed_units += 1
                        break  # Break the loop if any unit fails
                    elif int(unit_data["markstatus"]) == 0:
                        status = "pending"
                        break
                else:
                    status = "pending"
            average_mark = round(total_marks / num_units, 2) if num_units > 0 else 0
            student_data["status"] = status
            student_data["average_mark"] = average_mark

        status1 = "pass"
        i = 0
        for student_data in student_data_dict:
            if student_data["status"] != status1:
                pass
                # print(student_data["student_id"],"fail")
            else:

                student_id = int(student_data["student_id"])
                module_id = int(modid) + 1
                module_id2 = int(modid) + 2
                academic_year = int(academiyear) + 1

                # Check if the student is not already enrolled in the module
                enrollment_exists = StudentEnrollment.query.filter_by(
                    student_id=student_id,
                    module_id=module_id,
                    academic_year=academic_year,
                ).first()
                if enrollment_exists:
                    # flash('Student is already enrolled in the module.', 'warning')
                    pass
                else:
                    # Create a new enrollment
                    new_enrollment = StudentEnrollment(
                        student_id=student_id,
                        module_id=module_id,
                        academic_year=academic_year,
                    )
                    new_enrollment2 = StudentEnrollment(
                        student_id=student_id,
                        module_id=module_id2,
                        academic_year=academic_year,
                    )

                    db.session.add(new_enrollment)
                    db.session.add(new_enrollment2)
                    db.session.commit()
                    new_enrollment_id = new_enrollment.id
                    new_enrollment_id2 = new_enrollment2.id
                    enroll_units = Units.query.filter_by(module_id=module_id).all()
                    enroll_units2 = Units.query.filter_by(module_id=module_id2).all()

                    for unit in enroll_units:
                        new_unit_enrollment = EnrollmentUnits(
                            enrollment_id=new_enrollment_id, unit_id=unit.id
                        )
                        print(new_unit_enrollment)
                        db.session.add(new_unit_enrollment)
                        db.session.commit()
                        newmarkenrollmentid = new_unit_enrollment.id
                        print(newmarkenrollmentid)
                        new_unit_mark = Marks(unitenrollment_id=new_unit_enrollment.id)
                        db.session.add(new_unit_mark)
                        print(new_enrollment_id)
                    for unit in enroll_units2:
                        new_unit_enrollment = EnrollmentUnits(
                            enrollment_id=new_enrollment_id2, unit_id=unit.id
                        )
                        print(new_unit_enrollment)
                        db.session.add(new_unit_enrollment)
                        db.session.commit()
                        newmarkenrollmentid = new_unit_enrollment.id
                        print(newmarkenrollmentid)
                        new_unit_mark = Marks(unitenrollment_id=new_unit_enrollment.id)
                        db.session.add(new_unit_mark)
                        print(new_enrollment_id)
                    db.session.commit()
                    flash("Student enrolled successfully.", "success")

        for student_data in student_data_dict:
            #  print(student_data['names'])
            failed_units = 0
            missingmark = 0
            units = []
            for unit_data in student_data["values"] + student_data["valuesmod2"]:

                total_marks += unit_data["unit_mark"]
                num_units += 1
                if unit_data["markstatus"] != None:
                    if int(unit_data["markstatus"]) == 2:
                        status = "fail"
                        failed_units += 1
                        print(unit_data["unit"])
                        # units="there there"
                        units.append(unit_data["unit"])

                        # print((unit_data["markstatus"]))
                        # Break the loop if any unit fails
                    elif int(unit_data["markstatus"]) == 0:
                        status = "pending"
                        missingmark += 1
                        # print((unit_data["markstatus"]))
                        break

                    # print((unit_data["markstatus"]))
                    # print(failed_units,"failed_units")
                else:
                    status = "pending"
                    missingmark += 1

            if failed_units < 1 and missingmark < 1:
                recommendation = "Pass"
                Passlist.append(
                    {
                        "regno": student_data["reg"],
                        "name": student_data["names"],
                        "recommendation": recommendation,
                    }
                )
            elif failed_units < 4:
                recommendation = "Supplementary"
                Suppllementarylist.append(
                    {
                        "regno": student_data["reg"],
                        "name": student_data["names"],
                        "recommendation": recommendation,
                        "units": list(units),
                    }
                )
            elif failed_units == 4:
                ecommendation = "Repeat Year"
                Repeatyearlist.append(
                    {
                        "regno": student_data["reg"],
                        "name": student_data["names"],
                        "recommendation": recommendation,
                        "units": list(units),
                    }
                )
            elif failed_units > 4:
                recommendation = "Discontinuation"
                Discontinuationlist.append(
                    {
                        "regno": student_data["reg"],
                        "name": student_data["names"],
                        "recommendation": recommendation,
                        "units": units,
                    }
                )
        #  print(Passlist,'paslist',Suppllementarylist,'supps')

    length = len(tester)

    ln = len(student_data_dict)

    if type == "consosheet":
        print(student_data_dict)
        return render_template(
            "admin/consolidated.html",
            data=student_data_dict,
            length=ln,
            title="Consolidated Style Sheet",
        )

    elif type == "passlist":
        if Passlist:
            return render_template("admin/list.html", list=Passlist, title="Pass list")
        else:
            flash(
                "No marks have been submitted yet or No Students fall under this category "
            )
            return redirect(url_for("admin.adminDashboard"))
    elif type == "supplementary":
        if Suppllementarylist:

            return render_template(
                "admin/list.html", list=Suppllementarylist, title="Supplementary"
            )
        else:
            flash(
                "No marks have been submitted yet or No Students fall under this category "
            )
            return redirect(url_for("admin.adminDashboard"))
    elif type == "repeatyear":
        if Repeatyearlist:
            return render_template(
                "admin/list.html", list=Repeatyearlist, title="Repeat Year"
            )

        else:
            flash(
                "No marks have been submitted yet or No Students fall under this category "
            )
            return redirect(url_for("admin.adminDashboard"))
    elif type == "discontinuation":
        if Discontinuationlist:
            return render_template(
                "admin/list.html", list=Discontinuationlist, title="Discontinuation"
            )

        else:
            flash(
                "No marks have been submitted yet or No Students fall under this category "
            )
            return redirect(url_for("admin.adminDashboard"))
    print(student_data_dict)

    return render_template(
        "admin/consolidated.html",
        data=student_data_dict,
        length=ln,
        title="Consolidated Style Sheet",
    )


# Admin Dashboard
@admin.route("/admin/dashboard")
def adminDashboard():
    AcademicYears = (
        db.session.query(
            StudentEnrollment.academic_year.label("academicyears"),
            Modules.year.label("yearofstudy"),
        )
        .join(Modules, StudentEnrollment.module_id == Modules.id)
        .distinct()
        .all()
    )
    print(AcademicYears)
    return render_template(
        "admin/dashboard.html", title="Admin Dashboard", AcademicYears=AcademicYears
    )


@admin.route("/admin/editmarks", methods=["GET", "POST"])
@admin_required
def editMarks():
    if request.method == "GET":
        acyear = request.args.get("acyear")
        unit = request.args.get("unit")
        year = request.args.get("year")
        # acyear=20222023
        # unit=5
        print(acyear, unit)
        acadyear = acyear
        yunit = unit

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
                StudentEnrollment, EnrollmentUnits.enrollment_id == StudentEnrollment.id
            )
            .join(User, StudentEnrollment.student_id == User.id)
            .join(Units, EnrollmentUnits.unit_id == Units.id)
            .join(Marks, EnrollmentUnits.id == Marks.unitenrollment_id)
            .join(Modules, Units.module_id == Modules.id)
        )
        enrolledStudents = query.filter(
            Units.id == unit,
            StudentEnrollment.academic_year == acyear,
            Modules.year == year,
        )
        students = enrolledStudents.distinct()
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
        print(InMyUnit)

        return render_template("admin/editmarks.html", students=InMyUnit)

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
            enrollment_id, catmarks, assignmentmarks, practicalmarks, exammarks, mark_id
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
                    assignmentmarks = float(assignmentmarks) if assignmentmarks else 0
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

        return redirect(url_for("admin.adminDashboard"))


@admin.route("/admin/editmarks/years", methods=["GET"])
@admin_required
def getAcademicYears():
    AcademicYears = (
        db.session.query(
            StudentEnrollment.academic_year.label("academicyears"),
            Modules.year.label("yearofstudy"),
        )
        .join(Modules, StudentEnrollment.module_id == Modules.id)
        .distinct()
        .all()
    )
    print(AcademicYears)
    return render_template(
        "admin/Viewyears.html",
        title="Editable Academic Years",
        AcademicYears=AcademicYears,
    )


@admin.route("/admin/editmarks/years/units")
@admin_required
def getUnits():
    if request.method == "GET":
        acyear = request.args.get("acyear")
        yr = request.args.get("year")
        # acyear=20222024
        # yr=2
        print(acyear, yr)
        year_units = (
            db.session.query(
                Units.name.label("name"), Units.code.label("code"), Units.id.label("id")
            )
            .join(
                StudentEnrollment,
                Units.module_id == StudentEnrollment.module_id,
            )
            .join(Modules, Units.module_id == Modules.id)
            .filter(StudentEnrollment.academic_year == acyear, Modules.year == yr)
            .distinct()
            .all()
        )
        print(year_units)
        unit_details = []
        for unit in year_units:
            unit_details.append(
                {
                    "name": unit.name,
                    "code": unit.code,
                    "id": unit.id,
                }
            )
        # print(unit_details[0])  # Just for debugging

    return render_template(
        "admin/viewunits.html",
        acyear=acyear,
        yr=yr,
        year_units=unit_details,
        title="Edit Marks (Units)",
    )



@admin.route("/addunit", methods=["GET", "POST"])
@admin_required
def addunit():
    form = AddUnit()
    if form.validate_on_submit():
        unit_name = form.unit_name.data
        unit_code = form.unit_code.data
        module_id = form.module_id.data

        # Check if the student is not already enrolled in the module
        unit_exists = Units.query.filter_by(
            code=unit_code
        ).first()
        if unit_exists:
            flash("Unit  already exist.", "warning")
        else:
            # Create a new enrollment
            new_unit = Units(
                name=unit_name, module_id=module_id, code=unit_code
            )

            db.session.add(new_unit)
            db.session.commit()
    
            flash("Unit added successfully.", "success")

    return render_template(
        "admin/addunit.html", form=form, title="Create Unit"
    )
