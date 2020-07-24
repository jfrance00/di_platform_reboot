from github import Github
import flask
import requests
import mistune
import ast
from . import syllabus as syl
from . import forms, models, create_user
from . import app, db
import flask_login  # LoginManager, login_user, login_required, logout_user, current_user

syllabus = syl.Syllabus()


def get_course_description(param):
    pass


@app.route('/')
def index():
    """
    home page, shows the list of courses
    :return:
    """

    return flask.render_template('home.html', list_of_courses=syllabus.list_of_courses, course_data=syllabus.syllabuses)


@app.route('/profile/')
# @login.unauthorized()
def profile():
    users = models.User.query.all()
    return flask.render_template('profile.html', users=users)


# ----------------------login/out----------------------------------


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.Login()
    if flask.request.method == 'POST':  # does not work with "if form.validate_on_submit():"
        login_email = form.email.data
        user = models.User.query.filter_by(email=login_email).first()
        if user:  # verifies credentials against database
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


# ----------------------end of login/out----------------------------------

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


@app.route('/course/<course>')
def weeks(course):
    return flask.render_template('weeks.html', data=syllabus.syllabuses[course]['weeks'], course=course)


@app.route("/course/<course>/<week>")
def days(course, week):
    days_data = syllabus.syllabuses[course]['weeks'][week]['Days']
    others = syllabus.syllabuses[course]['weeks'][week]['other resources']
    return flask.render_template("days.html", data=days_data, others=others, course=course, week=week)


@app.route("/course/<course>/<week>/<day>")
def day(course, week, day):
    course_day = syllabus.syllabuses[course]['weeks'][week]['Days'][day]
    return flask.render_template("lesson.html", data=course_day, course=course, week=week, day=day)


def get_file_path(course, week, day, file):
    if day in ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"]:
        day = syllabus.syllabuses[course]['weeks'][week]['Days'][day]

        # check if file is "day" file or other resources

        for key, value in day.items():
            if key == "onsite":
                if file in value["Class Files"]:
                    file_type = "class"
                else:
                    file_type = "exercise"
            elif key == "online":
                if file in value['Exercises']:
                    file_type = "exercise"
            else:
                continue

        if file_type == "exercise":
            return syllabus.syllabuses[course]['weeks'][week]["Notion"] + "/Exercises/" + \
                   file + ".md"
        else:
            return syllabus.syllabuses[course]['weeks'][week]["Notion"] + "/" + \
                   file + ".md"

    elif day in syllabus.syllabuses[course]['weeks'][week]["other resources"]:

        return syllabus.syllabuses[course]['weeks'][week]["Notion"] + "/" + day + "/" +\
               file + ".md"


@app.route("/course/<course>/<week>/<day>/<file>")
def render_file(course, week, day, file):
    file_path = get_file_path(course, week, day, file)

    r = syllabus.repo
    cont = syllabus.repo.get_contents(file_path)
    r = requests.get(cont.download_url)
    return flask.render_template("exercise.html", data=mistune.markdown(r.text), course=course, week=week, day=day,
                                 file=file)
