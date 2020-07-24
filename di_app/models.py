import flask_sqlalchemy
from flask_login import UserMixin
from . import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(264))
    username = db.Column(db.String(264), unique=True)
    email = db.Column(db.String(264), unique=True)
    password = db.Column(db.String(264))
    #flagged_exercises = db.Column(db.


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
