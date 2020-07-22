from . import db, models, forms
import sqlalchemy


class CreateUser:
    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self.email = email
        self.password = password

    def save_signup_data(self):             #Redundant - info in view file, either figure out how to call function in view or delete
        # name = forms.CreateUser.name.data
        # email = forms.CreateUser.email.data
        # username = forms.CreateUser.username.data
        # password = forms.CreateUser.password.data
        return name, email, username, password

    def retrieve_data(self, data):
        pass