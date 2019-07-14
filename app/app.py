from flask import Flask,render_template,request,redirect,url_for,abort
from flask_login import LoginManager,login_user,logout_user,login_required,current_user
from app import key
from hashlib import sha256
from PIL import Image
import random,string
import os

app = Flask(__name__)
from app.models import db,Content,User,ContentGoodUser
login_manager = LoginManager()
login_manager.init_app(app)
app.config["SECRET_KEY"] = key.SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024;
app.config['UPLOAD_FOLDER'] = "/uploads"



@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


@app.route("/")
def index():
    contents = Content.query.join(User).order_by(Content.pub_date.desc()).all()
    if current_user.is_authenticated:
        content_good_users = ContentGoodUser.query.filter_by(user_id=current_user.id).all()
        good_content = []
        for content_good_user in content_good_users:
            good_content.append(content_good_user.content_id)
        for content in contents:
            if content.id in good_content:
                content.good = True
    return render_template("index.html", contents=contents)


@app.route("/content/<content_id>")
def content(content_id):
    content = Content.query.filter_by(id=content_id).join(User).all()[0]
    if current_user.is_authenticated:
        content_good_users = ContentGoodUser.query.filter_by(user_id=current_user.id,content_id=content_id).all()
        if len(content_good_users) >= 1:
            content.good = True
    return render_template("content.html",content=content)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login_submit",methods=["POST"])
def login_submit():
    user_name = request.form["user_name"]
    user = User.query.filter_by(name=user_name).first()
    if user is None:
        return redirect(url_for("login"))
    else:
        hashed_password = sha256((user_name + request.form["password"] + key.SALT).encode("utf-8")).hexdigest()
        if hashed_password != user.hashed_password:
            return redirect(url_for("login"))
        else:
            login_user(user)
            return redirect(url_for("index"))


@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")


@app.route("/sign_up_submit",methods=["POST"])
def sign_up_submit():
    user_name = request.form["user_name"]
    user = User.query.filter_by(name=user_name).first()
    if user is None:
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if password != confirm_password:
            return redirect(url_for("sign_up"))
        else:
            hashed_password = sha256((user_name + password + key.SALT).encode("utf-8")).hexdigest()
            new_user = User(name=user_name,hashed_password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("index"))
    else:
        return redirect(url_for("sign_up"))


@app.route("/mypage/<user_name>")
def mypage(user_name):
    user = User.query.filter_by(name=user_name).all()[0]
    contents = Content.query.filter_by(user_id=user.id).all()
    if current_user.is_authenticated:
        content_good_users = ContentGoodUser.query.filter_by(user_id=current_user.id).all()
        good_content = []
        for content_good_user in content_good_users:
            good_content.append(content_good_user.content_id)
        for content in contents:
            if content.id in good_content:
                content.good = True
    return render_template("mypage.html",user=user, contents=contents)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/edit/<content_id>")
@login_required
def edit(content_id):
    if content_id == "new":
        return render_template("edit.html")
    else:
        content = Content.query.filter_by(id=content_id).all()[0]
        if(content.user_id==current_user.id):
            return render_template("edit.html", content=content)
        else:
            return abort(404)


@app.route("/publish/<content_id>",methods=["POST"])
@login_required
def publish(content_id):
    title = request.form["title"]
    body = request.form["body"]
    if(content_id == "new"):
        content = Content(title=title,body=body,user_id=current_user.id)
        db.session.add(content)
        db.session.commit()
        return redirect(url_for("index"))
    else:
        content = Content.query.filter_by(id=content_id).all()[0]
        if content.user_id == current_user.id:
            content.title = title
            content.body = body
            db.session.commit()
            return redirect(url_for("index"))
        else:
            abort(404)


@app.route("/delete/<content_id>")
@login_required
def delete(content_id):
    content = Content.query.filter_by(id=content_id).all()[0]
    if content.user_id == current_user.id:
        db.session.delete(content)
        db.session.commit()
        return redirect(url_for("index"))
    else:
        abort(404)


@app.route("/config/<user_name>")
@login_required
def config(user_name):
    if user_name == current_user.name:
        return render_template("config.html")
    else:
        abort(404)


@app.route("/config_submit",methods=["POST"])
@login_required
def config_submit():
    user = User.query.filter_by(id=current_user.id).all()[0]
    user.name = request.form["name"]
    user.description = request.form["description"]
    icon = request.files["icon"]
    if icon.filename == "":
        db.session.add(user)
        db.session.commit()
    else:
        file_extension = icon.filename.rsplit('.', 1)[1]
        if file_extension in ["jpg","png"]:
            icon = Image.open(request.files["icon"])
            icon_resize = icon.resize((256,256))
            old_file_name = user.icon_file_name
            new_file_name = "".join(random.choices(string.ascii_letters+string.digits,k=20))+".jpg"
            user.icon_file_name = new_file_name
            db.session.add(user)
            db.session.commit()
            icon_resize.save("app/static/uploads/"+new_file_name)
            if (old_file_name is not None) and os.path.exists("app/static/uploads/"+old_file_name):
                os.remove("app/static/uploads/"+old_file_name)
        else:
            abort(404)
    return redirect("/mypage/" + current_user.name)


@app.route("/reset_password")
@login_required
def reset_password():
    return render_template("reset_password.html")


@app.route("/reset_password_submit",methods=["POST"])
@login_required
def submit_reset_password():
    hashed_now_password = sha256((current_user.name + request.form["now_password"] + key.SALT).encode("utf-8")).hexdigest()
    if hashed_now_password == current_user.hashed_password:
        hashed_new_password = sha256((current_user.name + request.form["new_password"] + key.SALT).encode("utf-8")).hexdigest()
        hashed_confirm_new_password = sha256((current_user.name + request.form["confirm_new_password"] + key.SALT).encode("utf-8")).hexdigest()
        if hashed_new_password == hashed_confirm_new_password:
            current_user.hashed_password = hashed_new_password
            db.session.add(current_user)
            db.session.commit()
            return redirect("/config/" + current_user.name)
    abort(404)


@app.route("/good", methods=["POST"])
@login_required
def good():
    content_id = request.json['content_id']
    content = Content.query.filter_by(id=content_id).all()[0]
    user_id = current_user.id
    content_good_user = ContentGoodUser.query.filter_by(content_id=content_id,user_id=user_id).all()
    if len(content_good_user) >= 1:
        db.session.delete(content_good_user[0])
        content.good_count = content.good_count - 1
    else:
        content_good_user = ContentGoodUser(content_id=content_id,user_id=user_id)
        db.session.add(content_good_user)
        content.good_count = content.good_count + 1
    db.session.commit()
    return str(content.good_count)


if __name__ == "__main__":
    app.run(debug=True)