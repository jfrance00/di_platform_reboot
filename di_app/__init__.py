import flask
import flask_sqlalchemy
import flask_migrate

app = flask.Flask(__name__)
<<<<<<< HEAD
app.config['SECRET_KEY'] = 'blahblahsecret'
=======
app.config['SECRET_KEY'] = "secretKey"

>>>>>>> e10be0f0848ffca6cbb32437d5f5051bd33d97a6

db = flask_sqlalchemy.SQLAlchemy(app)
migrate = flask_migrate.Migrate(app, db)

from . import views
