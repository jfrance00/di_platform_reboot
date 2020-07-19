import flask
from . import app

@app.route('/')
def index():
    return flask.render_template('home.html')

@app.route('/courses')    #get rid of this page because of course menu item
def courses():
    return flask.render_template('courses.html')

@app.route('/<course>/weeks')
def weeks(course):
    pass

@app.route('/<course>/days')
def days(course):
    pass

@app.route('/<course>/day<num>')
def lesson(course, day):
    pass

@app.route('/<course>/day<num>/<resource>')
def resource(course, day, resource):
    pass
