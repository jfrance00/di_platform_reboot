import flask
import requests
import mistune
from . import syllabus as syl
from . import forms, models, create_user
from . import app, db
import flask_login  # LoginManager, login_user, login_required, logout_user, current_user

# global parameter that initializes and downloads the syllabus of DI learning
syllabus = syl.Syllabus()


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


@app.route('/course/<course>')
def weeks(course):
    """
    Syllabus of a specific course
    :param course:
    :return:
    """
    return flask.render_template('weeks.html', data=syllabus.syllabuses[course]['weeks'], course=course)


@app.route("/course/<course>/<week>")
def days(course, week):

    """
    View of a specific week of a specific course

    :param course:
    :param week:
    :return:
    """
    days_data = syllabus.syllabuses[course]['weeks'][week]['Days']
    others = syllabus.syllabuses[course]['weeks'][week]['other resources']
    return flask.render_template("days.html", data=days_data, others=others, course=course, week=week)


@app.route("/course/<course>/<week>/<day>/<file>")
def render_file(course, week, day, file):
    """
    Download and view the contend of a course file.
    :param course:
    :param week:
    :param day:
    :param file:
    :return:
    """
    file_path = syllabus.get_file_path(course, week, day, file)
    try:
        cont = syllabus.repo.get_contents(file_path)
    except:
        flask.flash("The requested file is not available, please contact administrator", "missing file")
        return days(course, week)
    else:
        r = requests.get(cont.download_url)
    return flask.render_template("exercise.html", data=mistune.markdown(r.text), course=course, week=week, day=day,
                                 file=file)
