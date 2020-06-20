from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_urlsafe
from datetime import datetime
from flask_login.mixins import UserMixin
from app import db, login


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    session_token = db.Column(db.String(43), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, passwod):
        self.password_hash = generate_password_hash(passwod, salt_length=14)

    def check_password(self, passwod):
        return check_password_hash(self.password_hash, passwod)

    def get_id(self):
        return self.session_token

    def set_session_token(self):
        self.session_token = token_urlsafe()
        db.session.commit()


@login.user_loader
def load_user(session_token):
    return User.query.filter_by(session_token=session_token).first()


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Post {self.body}>'
