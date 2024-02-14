from datetime import datetime

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from config import config

db=SQLAlchemy()
bootstrap = Bootstrap()

def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    bootstrap.init_app(app)

    from .main import rms as rms_blueprint
    app.register_blueprint(rms_blueprint)

    from .authentication import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    return app

