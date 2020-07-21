<<<<<<< HEAD
import flask
from . import forms, models
from . import app, db

=======
import json
from github import Github
import flask
import requests
import markdown
import mistune
import ast

from . import app
from . import forms, models
from . import app, db

token = ''  # here comes token!! need to understand how to keep it secured and still online
owner = 'arturisto'
g = Github(token)
u = g.get_user()
repo = u.get_repo("DI-Learning-Exercises")

>>>>>>> e10be0f0848ffca6cbb32437d5f5051bd33d97a6

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

<<<<<<< HEAD
=======

@app.route('/test')
def github_test():
    # get syllabus data
    cont = repo.get_contents("syllabus.json")
    byte_str = cont.decoded_content
    dict_str = byte_str.decode("UTF-8")
    syllabus = ast.literal_eval(dict_str)
    flask.session['syllabus'] = syllabus
    print(repr(syllabus))
    # r = requests.get(cont.download_url)
    # html = flask.Markup(markdown.markdown(r.text))
    x = 3
    # return flask.render_template("github_test.html", data = mistune.markdown(r.text))
    return flask.render_template("github_test.html", data=syllabus, show="courses")


@app.route("/course/<course>")
def render_course(course):
    course_syllabus = flask.session['syllabus'][course]
    return flask.render_template("github_test.html", data=course_syllabus, show="weeks", course=course)


@app.route("/course/<course>/<week>")
def render_week(course, week):
    course_week = flask.session['syllabus'][course][week]

    return flask.render_template("github_test.html", data=course_week, show="days", course=course, week=week)


@app.route("/course/<course>/<week>/<day>")
def render_day(course, week, day):
    course_day = flask.session['syllabus'][course][week][day]

    return flask.render_template("github_test.html", data=course_day, show="specific_day", course=course, week=week,
                                 day=day)


@app.route("/course/<course>/<week>/<day>/<file>")
def render_file(course, week, day, file):
    path = flask.session['syllabus'][course][week]["Notion"] + "/" + flask.session['syllabus'][course][week][day][
        file] + ".md"
    cont = repo.get_contents(path)

    r = requests.get(cont.download_url)
    # html = flask.Markup(markdown.markdown(r.text))
    return flask.render_template("github_test.html", data=mistune.markdown(r.text), show="file")

>>>>>>> e10be0f0848ffca6cbb32437d5f5051bd33d97a6
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
<<<<<<< HEAD
=======

>>>>>>> e10be0f0848ffca6cbb32437d5f5051bd33d97a6
