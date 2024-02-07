from flask import Blueprint
from flask import request,render_template,redirect,flash,jsonify,url_for
from ..models import User
from app import db
from . import auth
from werkzeug.security import generate_password_hash,check_password_hash



@auth.route("/user/signup", methods = ['POST', 'GET'])
def userSignUp():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        username = request.form.get('username')
        edu = request.form.get('edu')
        password = request.form.get('password')

        # check that all the fields are filled
        if fname == "" or lname == "" or lname == "" or email == "" or password == "" or username == "" or edu == "":
            flash('Please fill all the fields', 'danger')
            return redirect('/user/signup')
        else:
            hash_password = generate_password_hash(password)
            user = User(fname = fname, lname = lname, email = email, password = hash_password, edu = edu, username = username)
            db.session.add(user)
            db.session.commit()
            print(user)
            flash('Acount created successfully Admin will approve your account in 10 to 30 min', 'success')
            return ("Something goes here ")
    else:
        return render_template('User/signup.html', title ="User signup")
    
@auth.route("/user/login", methods=['GET','POST'])
def userLogin():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        print(email + password)
        if email=="" or password=="":
            flash("Please fill in all the Fields")
            return redirect(url_for('auth.userLogin'))
        else:
           print(email + password)
           user = User.query.filter_by(email=email).first()
           if user and check_password_hash(user.password, password):
            # Successful login
            flash("Login successful", 'success')
            return ("YOU ARE LOGGED IN AS " + email)
  
    return render_template('user/login.html', title="user login")

