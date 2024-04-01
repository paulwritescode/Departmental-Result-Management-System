import os

from flask_migrate import Migrate

from app import create_app, db
from app.models import User, Units, Role, Modules, StudentEnrollment, EnrollmentUnits, LecturerAssignment, Marks, Status

app = create_app("default")
migrate = Migrate(app, db)
# db.create_all()


@app.shell_context_processor
def make_shellprocessor():
    return dict(db=db)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        Role.insert_roles()
        Units.insert_units()

    app.run(debug=True)
