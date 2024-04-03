import os
from dotenv import load_dotenv

from flask_migrate import Migrate

from app import create_app, db
from app.models import  Units, Role
app = create_app("default")
migrate = Migrate(app, db)
# db.create_all()


@app.shell_context_processor
def make_shellprocessor():
    return dict(db=db)


@app.cli.command()
def deploy():

    db.create_all()

    Role.insert_roles()

    Units.insert_units()
