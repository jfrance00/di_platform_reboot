<<<<<<< HEAD
import json
from github import Github
import flask
import requests
import markdown
import mistune
import ast

from . import app

token = ''  # here comes token!! need to understand how to keep it secured and still online
owner = 'arturisto'
g = Github(token)
u = g.get_user()
repo = u.get_repo("DI-Learning-Exercises")



@app.route('/')
def index():
    return flask.render_template('home.html')


@app.route('/courses')
def courses():
    return flask.render_template('courses.html')


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
