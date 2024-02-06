from flask import Flask, render_template

app = Flask(__name__)

# login route
@app.route("/")
def login():
    return render_template('login.html')


# admin route
@app.route("/admin/")
def adminRoute():
    return render_template('admin/index.html')

# user route
@app.route("/user/")
def userRoute():
    return render_template('user/index.html')
