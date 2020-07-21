import flask
from . import forms, models
from . import app, db


@app.route('/')
def index():
    return flask.render_template('home.html')


@app.route('/profile')
def profile():
    return flask.render_template('profile.html')


@app.route('/login')
def login():
    form = forms.CreateUser()
    return flask.render_template('login.html', form=form)

@app.route('/course/weeks') #TODO course will be turned into a variable to pull relevant data
def weeks():
    course = {              # !Temporary! data will come from database
        'length_in_weeks': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'days_of_week': [1, 2, 3, 4, 5],
    }
    return flask.render_template('weeks.html', course=course)


@app.route('/course/weeknum/days')  #TODO course variable
def days():
    course = {              # !Temporary! data will come from database
        'length_in_weeks': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'days_of_week': [1, 2, 3, 4, 5],
    }
    return flask.render_template('days.html', course=course)


@app.route('/course/weeknum/daynum')  #TODO course variable and day #
def lesson():
    course = {  # !Temporary! data will come from database
        'length_in_weeks': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'days_of_week': [1, 2, 3, 4, 5],
        'lesson_activities': ['Lecture1', 'Lecture2', 'xp', 'xp gold', 'xp ninja', 'Daily']
    }
    return flask.render_template('lesson.html', course=course)


@app.route('/course/daynum/resource')  #TODO course variable, day#, resource all variables
def exercise():
    return flask.render_template('exercise.html')
