from datetime import datetime

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import config

db=SQLAlchemy()
bootstrap = Bootstrap()
login_manager=LoginManager()

login_manager.login_view="auth.userLogin"

def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .authentication import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)
    

    from .lecturer import lecturer as lecturer_blueprint
    app.register_blueprint(lecturer_blueprint)
    


    return app

