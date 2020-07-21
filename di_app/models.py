import flask_sqlalchemy
from . import db


class CreateUserData(db.Model):
    name = db.Column(db.String)
    user_name = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
