import flask_wtf
import wtforms as wtf
import flask_sqlalchemy
import email_validator
from wtforms import validators as valid

class CreateUser(flask_wtf.FlaskForm):
    name = wtf.StringField('Name', [valid.InputRequired(message="Name required for signup")])
    user_name = wtf.StringField('User Name', [valid.InputRequired(message="Username required for signup")])
    email = wtf.StringField('Email', [valid.Email(message="Must enter valid email address")])
    password = wtf.PasswordField("Password", [valid.InputRequired(message="Must enter a password")])
    confirm_pass = wtf.PasswordField("Confirm Password", [valid.EqualTo(password, message="Passwords must match")])
