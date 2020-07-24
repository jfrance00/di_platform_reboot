import json
from github import Github
import flask
import requests
import markdown
import mistune
import ast
import sqlite3
import flask_login #LoginManager, login_user, login_required, logout_user, current_user


from . import forms, models, create_user
from . import app, db

token = '0f5e35b4304339db5b61e05499a2a1babec0a395'  # here comes token!! need to understand how to keep it secured and still online
owner = 'arturisto'
g = Github(token)
u = g.get_user()
repo = u.get_repo("DI-Learning-Exercises")


@app.route('/')
def index():
    return flask.render_template('home.html')


@app.route('/profile/')
# @login.unauthorized()
def profile():
    users = models.User.query.all()
    return flask.render_template('profile.html', users=users)


#----------------------login/out----------------------------------


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.Login()
    if flask.request.method == 'POST':       # does not work with "if form.validate_on_submit():"
        login_email = form.email.data
        user = models.User.query.filter_by(email=login_email).first()
        if user:                                   # verifies credentials against database
            if user.password == form.password.data:
                create_user.load_user(user.id)
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                flask_login.login_user(user, remember=True)
                return flask.redirect(flask.url_for('profile'))
    return flask.render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    user = models.load_user()
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    flask_login.logout_user()
    print(user.authenticated)
    return flask.redirect('login')


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
@flask_login.login_required
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

