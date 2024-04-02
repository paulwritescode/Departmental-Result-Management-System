from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from werkzeug.security import check_password_hash, generate_password_hash

from app import db

from ..models import User
from . import auth
from .forms import LoginForm, RegisterForm


@auth.before_app_request
def before_request():
    excluded_endpoints = ["auth.userLogin", "auth.userSignUp", "static"]
    if not current_user.is_authenticated and request.endpoint not in excluded_endpoints:
        return redirect(url_for("auth.userLogin"))


@auth.route("/base", methods=["POST", "GET"])
@login_required
def base():
    return render_template("layout.html")


@auth.route("/admin/signup", methods=["POST", "GET"])
def userSignUp():
  
    reg_form = RegisterForm()
    if request.method == 'POST':
      print( reg_form.fname.data,
       reg_form.lname.data,
         reg_form.email.data,
        reg_form.role.data,
        reg_form.password.data,
        reg_form.username.data)
      if reg_form.validate_on_submit():
        print('anything')
        fname = reg_form.fname.data
        lname = reg_form.lname.data
        email = reg_form.email.data
        role = reg_form.role.data
        password = reg_form.password.data
        username = reg_form.username.data
        hash_password = generate_password_hash(password)
        user = User(fname=fname, lname=lname, email=email, password=hash_password, role_id=role, username=username)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully. Admin will approve your account in 10 to 30 min', 'success')
        return redirect(url_for('auth.userLogin'))
      else:
       
        for field, errors in reg_form.errors.items():
             print("somrthing")
             
             flash(f'Form validation failed. Please check your input.{field,errors}', 'danger')
        return redirect(url_for("auth.userSignUp"))
      print("something_else")
    return render_template('admin/signup.html', form=reg_form, title="User signup")



# Landing page User login
@auth.route("/login", methods=["GET", "POST"])
def userLogin():
    log_form = LoginForm()
    if request.method == "POST" and log_form.validate_on_submit():
        # Form submitted and validated successfully
        email = log_form.email.data
        password = log_form.password.data
        user = User.query.filter_by(email=email).first()
        if user is not None and check_password_hash(user.password, password):
            login_user(user)
            if current_user.is_authenticated and current_user.role.name == "Lecturer":
                return redirect(url_for("lecturer.home"))
            elif current_user.is_authenticated and current_user.role.name == "User":
                return render_template("user/studentdashboard.html")
                return "welcome Student"
            elif current_user.is_authenticated and current_user.role.name == "ADMIN":
                return redirect(url_for("admin.adminDashboard"))

            else:
                return "invalid role"
        else:
              flash("Error ocurred")
              print(check_password_hash(user.password, password))
    return render_template('login/login.html', form=log_form, title = 'System Login')



# Logout function
@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.userLogin"))
