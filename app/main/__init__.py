from flask import Blueprint


rms=Blueprint("rms",__name__)
from . import views