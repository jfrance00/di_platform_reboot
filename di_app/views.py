import flask
from . import app

@app.route('/')
def index():
    return flask.render_template('home.html')

@app.route('/courses')
def courses():
    return flask.render_template('courses.html')
