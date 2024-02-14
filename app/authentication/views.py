from flask import request,render_template,redirect,flash,jsonify,url_for
from ..models import User
from .forms import RegisterForm,LoginForm
from app import db
from . import auth
from flask_login import login_user,LoginManager,login_required,logout_user,current_user
from werkzeug.security import generate_password_hash,check_password_hash

@auth.before_app_request
def before_request():
    excluded_endpoints = ['auth.userLogin', 'auth.userSignUp', 'static']

    if not current_user.is_authenticated and request.endpoint not in excluded_endpoints:
        return redirect(url_for('auth.userLogin'))


@auth.route("/base",  methods=['POST', 'GET'])
@login_required
def base():
   return render_template("layout.html")


@auth.route("/user/signup", methods=['POST', 'GET'])
def userSignUp():
    print("blah this should appear")
    reg_form = RegisterForm()  
    if request.method == 'POST':
      if reg_form.validate_on_submit():
        print("Validation successful")
        print("validation on going ")
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
        print("Form validation failed") 
        for field, errors in reg_form.errors.items():
            print(f"Validation error for {field}: {errors}")
        flash('Form validation failed. Please check your input.', 'danger')
        return redirect(url_for("auth.userSignUp"))

    return render_template('User/signup.html', form=reg_form, title="User signup")
  
@auth.route("/user/login", methods=['GET','POST'])
def userLogin():
    log_form=LoginForm()
    if request.method == 'POST' and log_form.validate_on_submit():
        # Form submitted and validated successfully
        
        email = log_form.email.data
        password = log_form.password.data
        user = User.query.filter_by(email = email).first()
        if user is not None and check_password_hash(user.password, password ):
              login_user(user)
              return redirect(url_for("main.home"))  
        else:
              print("Error ocurred")
              print(check_password_hash(user.password, password))

                   
       
    return render_template('user/login.html', form=log_form)


@auth.route("/logout")
def logout():
    logout_user()

    return redirect(url_for('auth.userLogin'))
# if user has not logged in 


