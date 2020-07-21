import flask
import flask_sqlalchemy
import flask_migrate

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'blahblahsecret'

db = flask_sqlalchemy.SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)

from . import views
