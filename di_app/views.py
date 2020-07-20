import flask
from . import app


@app.route('/')
def index():
    return flask.render_template('home.html')


@app.route('/courses')    #get rid of this page because of course menu item
def courses():
    return flask.render_template('courses.html')


@app.route('/course/weeks') #TODO course will be turned into a variable to pull relevant data
def weeks():
    return flask.render_template('weeks.html')


@app.route('/course/weeknum/days')  #TODO course variable
def days():
    return flask.render_template('days.html')


@app.route('/course/weeknum/daynum')  #TODO course variable and day #
def lesson():
    return flask.render_template('lesson.html')


@app.route('/course/daynum/resource')  #TODO course variable, day#, resource all variables
def exercise():
    return flask.render_template('exercise.html')
