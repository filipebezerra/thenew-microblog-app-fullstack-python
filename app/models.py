import jwt
from secrets import token_urlsafe
from hashlib import md5
from datetime import datetime
from time import time
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login.mixins import UserMixin
from app import db, login

followers = db.Table('followers',
                     db.Column('follower_id', db.Integer,
                               db.ForeignKey('users.id')),
                     db.Column('followed_id', db.Integer,
                               db.ForeignKey('users.id'))
                     )


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    session_token = db.Column(db.String(43), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

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

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?s={size}&d=retro'

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    @property
    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self):
        expires_at = time() + \
            int(current_app.config['PASSWORD_RESET_EXPIRES_AT'])
        token = jwt.encode(
            {'reset_password': self.id, 'exp': expires_at},
            current_app.config['SECRET_KEY'], algorithm='HS256')
        return token.decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            user_id = jwt.decode(token, current_app.config['SECRET_KEY'],
                                 algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(user_id)


@login.user_loader
def load_user(session_token):
    return User.query.filter_by(session_token=session_token).first()


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    language = db.Column(db.String(5))

    def __repr__(self):
        return f'<Post {self.body}>'
