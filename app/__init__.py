from datetime import datetime
<<<<<<< HEAD

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from config import config

=======
from flask_login import LoginManager
>>>>>>> refs/remotes/origin/main
db=SQLAlchemy()
bootstrap = Bootstrap()
login_manager=LoginManager()

login_manager.login_view="auth.userLogin"

def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)
<<<<<<< HEAD
    bootstrap.init_app(app)

    from .main import rms as rms_blueprint
    app.register_blueprint(rms_blueprint)

=======
    login_manager.init_app(app)

    



    bootstrap.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
>>>>>>> refs/remotes/origin/main
    from .authentication import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    


    return app

