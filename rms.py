import os
from app import create_app, db
from flask_migrate import Migrate

app=create_app('default')
migrate=Migrate(app,db)
# db.create_all()




@app.shell_context_processor
def make_shellprocessor():
    return dict(db=db)


if __name__=="__main__":
    with app.app_context():
        db.create_all()    
    app.run(debug=True)
    