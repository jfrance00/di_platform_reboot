import flask
import flask_sqlalchemy
import flask_migrate

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = "secretKey"


db = flask_sqlalchemy.SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)

from . import views
