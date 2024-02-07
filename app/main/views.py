from . import rms
from flask import  redirect,render_template,request,url_for


@rms.route('/')
def home():
    return("this is the initial bootstrap")