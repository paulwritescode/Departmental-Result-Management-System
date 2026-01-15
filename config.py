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
    # Using SQLite for development (simpler setup)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///results.db'
    
    # Uncomment below for PostgreSQL
    # DATABASE_HOSTNAME=os.environ.get("DATABASE_HOSTNAME")
    # DATABASE_PORT=5432
    # DATABASE_PASSWORD=os.environ.get("DATABASE_PASSWORD")
    # DATABASE_NAME=os.environ.get("DATABASE_NAME")
    # DATABASE_USERNAME=os.environ.get("DATABASE_USERNAME")
    # SQLALCHEMY_DATABASE_URI = f'postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}'

    @staticmethod
    def init_app(app):
        pass


config = {"development": DevelopmentConfig, "default": DevelopmentConfig}
