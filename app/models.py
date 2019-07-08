from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from app.app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@localhost/tutorial_blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    good_count = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    user = db.relationship('User',backref=db.backref('content', lazy=True))

    def __repr__(self):
        return '<Content %r>' % self.title

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    hashed_password = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return '<User %r>' % self.name
