import flask_sqlalchemy
from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(264))
    username = db.Column(db.String(264), unique=True)
    email = db.Column(db.String(264), unique=True)
    password = db.Column(db.String(264))
    #flagged exercises
