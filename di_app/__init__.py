import flask
import flask_sqlalchemy
import flask_migrate

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = "secretKey"

from . import views
