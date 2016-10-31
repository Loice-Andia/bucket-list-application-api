import passlib
from app import db
from datetime import datetime
from sqlalchemy_utils import PasswordType


class Users(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(PasswordType(onload=lambda **kwargs: dict(
        schemes=[
            'pbkdf2_sha512',
            'md5_crypt'
        ],
        deprecated=['md5_crypt'],
        **kwargs
    ), ), unique=False, nullable=False)

    def verify_password(self, password):

        return self.password == password


class Bucketlists(db.Model):

    __tablename__ = "bucketlists"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), unique=True)
    description = db.Column(db.String(1000))
    time_created = db.Column(
        db.DateTime(timezone=True),
        default=datetime.utcnow)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    creator = db.relationship('Users',
                              backref=db.backref('bucketlists',
                                                 lazy='dynamic'))


class Items(db.Model):

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), unique=True)
    description = db.Column(db.String(1000))
    completed = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))
    bucketlist = db.relationship('Bucketlists',
                                 backref=db.backref('items', lazy='dynamic'))
