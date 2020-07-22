import flask
import flask_sqlalchemy
import flask_migrate
import os


app = flask.Flask(__name__)

app.config['SECRET_KEY'] = "secretKey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.getcwd(), 'user.db')

db = flask_sqlalchemy.SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)

from . import views, models



