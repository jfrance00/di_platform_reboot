import flask
import flask_sqlalchemy
import flask_migrate
from flask_login import LoginManager
import os


app = flask.Flask(__name__)

app.config['SECRET_KEY'] = "secretKey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'user.db')
login_manager = LoginManager()

db = flask_sqlalchemy.SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)

login_manager.init_app(app)
login_manager.login_view = 'login'

from . import views, models



