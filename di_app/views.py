from github import Github
import flask
import requests
import mistune
import ast

from . import forms, models, create_user
from . import app, db
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

token = '1625be1949a00603fa29bfda296abf1ca19876d2'  # here comes token!! need to understand how to keep it secured and still online
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


def save_lesson(course, week, day):      #saves same variables passed to lesson page where card is initially displayed
    resource_url = flask.url_for('lesson', course=course, week=week, day=day)
    data = flask.session['syllabus']["weeks"][week]['Days'][day]
    lesson_dict = {
        'URL': resource_url,
        'course': course,
        'week': week,
        'day': day,
        # 'data': data  TODO check if it makes sense to save data as part of dict, or to reference data object when making the card
    }
    current_user.flagged.append(lesson_dict)
    db.session.commit()




@app.route('/')
def index():
    """
    home page, shows the list of courses
    :return:
    """

    flask.session['list_of_courses'] = get_list_of_courses()  # store the dict in the session for future use
    return flask.render_template('home.html', data=flask.session['list_of_courses'])


@app.route('/profile/')
def profile():
    users = models.User.query.all()
    active_user = current_user

    course_day = flask.session['syllabus']["weeks"][week]['Days'][day]
    #lesson.html", data=course_day, course=course, week=week, day=day)

    return flask.render_template('profile.html', users=users, current_user=current_user)


#----------------------login/out----------------------------------

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = forms.CreateUser()
    if flask.request.method == "POST":
    # if form.validate_on_submit():
        new_user = models.User()
        new_user.is_authenticated = False
        form.populate_obj(new_user)
        db.session.add(new_user)
        db.session.commit()
        return flask.redirect('login')
    return flask.render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.Login()
    if flask.request.method == 'POST':       # does not work with "if form.validate_on_submit():"
        login_email = form.email.data
        user = models.User.query.filter_by(email=login_email).first()
        if user:                                   # verifies credentials against database
            if user.password == form.password.data:
                models.load_user(user.id)
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return flask.redirect(flask.url_for('profile'))
    return flask.render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    user = models.load_user(current_user.id)
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    print(user.authenticated)
    return flask.redirect('login')


@app.route('/course/<course>')  # TODO course will be turned into a variable to pull relevant data
def weeks(course):
    course_path = "courses/" + course + ".json"
    cont = repo.get_contents(course_path)  # get syllabus
    byte_str = cont.decoded_content  # decoded repo data
    dict_str = byte_str.decode("UTF-8")  # parse the bytes to string
    syllabus = ast.literal_eval(dict_str)  # eval string to dict
    flask.session['syllabus'] = syllabus
    return flask.render_template('weeks.html', data=flask.session['syllabus']["weeks"], course=course)


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
@login_required
def render_course(course):
    course_syllabus = flask.session['syllabus'][course]
    return flask.render_template("github_test.html", data=course_syllabus, show="weeks", course=course)


@app.route("/course/<course>/<week>")
@login_required
def days(course, week):
    days_data = flask.session['syllabus']["weeks"][week]['Days']
    others = flask.session['syllabus']["weeks"][week]['other resources']
    return flask.render_template("days.html", data=days_data, others=others, course=course, week=week)


@app.route("/course/<course>/<week>/<day>")
@login_required
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
@login_required
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


@app.route('/flag_item', methods=['GET', 'POST'])
def flag_item(course, week, day):
    save_lesson(course, week, day)
    return flask.redirect('day')     # once function called redirects user back to page where lesson items listed
                                     # (I think it is 'day')


