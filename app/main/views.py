from . import main
from flask import request,render_template,redirect,flash,jsonify,url_for
from flask_login import login_user,LoginManager,login_required,logout_user,current_user
from flask import  redirect,render_template,request,url_for
from ..models import Permission
from ..decorators import admin_required, permission_required


@main.route('/')
@login_required
@permission_required(Permission.VIEW)
def home():
    return render_template("user/index.html")