import os


class Config:
    SECRET_KEY = "mysecret_key"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASKY_ADMIN = os.environ.get("FLASKY_ADMIN")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///results.db"


config = {"development": DevelopmentConfig, "default": DevelopmentConfig}
