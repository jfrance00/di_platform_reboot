from github import Github
import flask
import requests
import mistune
import ast
import urllib.parse
from . import forms
from . import app
import string

token = '0f5e35b4304339db5b61e05499a2a1babec0a395'  # here comes token!! need to understand how to keep it secured and still online
owner = 'arturisto'
g = Github(token)
u = g.get_user()
repo = u.get_repo("DI-Learning-Exercises")


def create_dict_of_courses(syllabus):
    """
    Create a dict of courses out of the syllabus.
    The dict is used for dynamicly create the dropdown nav bar of the courses
    :param syllabus:
    :return:
    """
    courses = dict()
    for key, value in syllabus.items():
        if "Python" in key:
            if "Python" in courses:
                courses["Python"].append(key)
            else:
                courses["Python"] = [key]
        elif "Java" in key:
            if "Java" in courses:
                courses["Java"].append(key)
            else:
                courses["Java"] = [key]
        else:
            if "Other" in courses:
                courses["Other"].append(key)
            else:
                courses["Other"] = [key]
    return courses


def get_list_of_courses():
    """
    Get list of courses on github in the courses folder
    :return:
    """
    list_of_courses = []
    cont = repo.get_contents("courses")
    for item in cont:
        name = item.name
        list_of_courses.append(name.strip(".json"))
    return list_of_courses


@app.route('/')
def index():
    """
    home page, shows the list of courses
    :return:
    """

    flask.session['list_of_courses'] = get_list_of_courses()  # store the dict in the session for future use
    # flask.session['dict_of_courses'] = create_dict_of_courses(syllabus)
    #
    return flask.render_template('home.html', data=flask.session['list_of_courses'])


@app.route('/profile')
def profile():
    return flask.render_template('profile.html')


@app.route('/login')
def login():
    form = forms.CreateUser()
    return flask.render_template('login.html', form=form)


@app.route('/course/<course>')  # TODO course will be turned into a variable to pull relevant data
def weeks(course):
    course_path = "courses/" + course + ".json"
    cont = repo.get_contents(course_path)  # get syllabus
    byte_str = cont.decoded_content  # decoded repo data
    dict_str = byte_str.decode("UTF-8")  # parse the bytes to string
    syllabus = ast.literal_eval(dict_str)  # eval string to dict
    flask.session['syllabus'] = syllabus
    return flask.render_template('weeks.html', data=flask.session['syllabus']["weeks"], course=course)


@app.route("/course/<course>/<week>")
def days(course, week):
    days_data = flask.session['syllabus']["weeks"][week]['Days']
    others = flask.session['syllabus']["weeks"][week]['other resources']
    return flask.render_template("days.html", data=days_data, others=others, course=course, week=week)


@app.route("/course/<course>/<week>/<day>")
def day(course, week, day):
    course_day = flask.session['syllabus']["weeks"][week]['Days'][day]
    return flask.render_template("lesson.html", data=course_day, course=course, week=week, day=day)


def get_file_type(week, day, file):
    day = flask.session['syllabus']["weeks"][week]['Days'][day]
    for key, value in day.items():
        if key == "onsite":
            if file in value["Class Files"]:
                return "class"
            else:
                return "exercise"
        elif key == "online":
            if file in value['Exercises']:
                return "exercise"
        else:
            continue


@app.route("/course/<course>/<week>/<day>/<file>")
def render_file(course, week, day, file):
    file_type = get_file_type(week, day, file)
    if file_type == "exercise":
        path = flask.session['syllabus']["weeks"][week]["Notion"] + "/Exercises/" + \
               file + ".md"
    else:
        path = flask.session['syllabus']["weeks"][week]["Notion"] + "/" + \
               file + ".md"

    cont = repo.get_contents(path)
    r = requests.get(cont.download_url)
    return flask.render_template("exercise.html", data=mistune.markdown(r.text), course=course, week=week, day=day,
                                 file=file)
