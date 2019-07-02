from flask import Flask,render_template,request,redirect,url_for
from flask_login import LoginManager,login_user,logout_user,login_required,UserMixin
from app import key
from hashlib import sha256

app = Flask(__name__)
from app.models import db,Content,User#,AuthUser
"""
login_manager = LoginManager()
login_manager.init_app(app)
app.config["SECRET_KEY"] = key.SECRET_KEY
"""

"""
@login_manager.user_loader
def load_user(id):
    return AuthUser.query.filter_by(id=id).first()
"""

@app.route("/")
def index():
    contents = Content.query.join(User).all()
    return render_template("index.html",contents=contents)


@app.route("/content/<content_id>")
def content(content_id):
    content = Content.query.filter_by(id=content_id).join(User).all()[0]
    return render_template("content.html",content=content)

"""
@app.route("/login")
def login():
    render_template("login.html")


@app.route("/login_submit",methods=["POST"])
def login_submit():
    user_name = request.form["user_name"]
    user = User.query.filter_by(name=user_name).first()
    if user is None:
        redirect(url_for("login"))
    else:
        hashed_password = sha256((user_name + request.form["password"] + key.SALT).encode("utf-8")).hexdigest()
        if hashed_password != user.hashed_password:
            redirect(url_for("login"))
        else:
            login_user(user.id)
            redirect(url_for(""))


@app.route("/sign_up")
def sign_up():
    render_template("sign_up.html")


@app.route("/sign_up_submit")
def sign_up_submit():
    user_name = request.form["user_name"]
    user = User.query.filter_by(name=user_name).first()
    if user is None:
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if password != confirm_password:
            redirect(url_for("sign_up"))
        else:
            hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
            new_user = User(name=user_name,hashed_password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            redirect(url_for(""))
    else:
        redirect(url_for("/sign_up"))


@app.route("/mypage")
@login_required
def mypage():
    render_template("mypage.html")
"""


if __name__ == "__main__":
    app.run(debug=True)