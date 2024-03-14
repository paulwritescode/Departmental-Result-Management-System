from flask import Blueprint
from ..models import Permission



lecturer=Blueprint("lecturer",__name__)
from . import views

@lecturer.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)