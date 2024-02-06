from flask import Flask, render_template

app = Flask(__name__)

# login route
@app.route("/")
def login():
    return render_template('login.html')
