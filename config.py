import os


class Config:
    SECRET_KEY = "mysecret_key"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASKY_ADMIN = os.environ.get("FLASKY_ADMIN")


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG=True

    SQLALCHEMY_DATABASE_URI = f'postgresql://postgres:root@localhost:5432/elimusawa'


config = {"development": DevelopmentConfig, "default": DevelopmentConfig}
