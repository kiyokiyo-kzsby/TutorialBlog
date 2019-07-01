from flask import Flask,render_template
from app.models import db,Content,User

app = Flask(__name__)


@app.route("/")
def index():
    render_template("index.html",login=login,contents=contents)


@app.route("/login")
def login():
    render_template("login.html")


@app.route("/login_submit")
def login():
    render_template()


@app.route("/register")
def login():
    render_template("register.html")


@app.route("/login_submit")
def login():
    render_template()


@app.route("/mypage")
def mypage():
    render_template("mypage.html")



if __name__ == "__main__":
    app.run(debug=True)