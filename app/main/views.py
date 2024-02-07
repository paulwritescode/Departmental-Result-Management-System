from . import rms
from flask import  redirect,render_template,request,url_for


@rms.route('/')
def home():
    return redirect(url_for("auth.userLogin"))