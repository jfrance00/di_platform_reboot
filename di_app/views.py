import json
from github import Github
import flask
import requests

from . import app

@app.route('/')
def index():
    return flask.render_template('home.html')

@app.route('/courses')
def courses():
    return flask.render_template('courses.html')


@app.route('/test')
def github_test():
    token = '' #here comes token!! need to understand how to keep it secured and still online
    owner = 'arturisto'
    repo = 'DI-Learning-Exercises'
    g = Github(token)
    u = g.get_user()
    x = u.login
    repo = u.get_repo("DI-Learning-Exercises")
    cont = repo.get_contents("Week 4/Day 1/Daily challenge.md")
    print (repo.name)
    # for repo_item in repo:
    #     print (repo_item.name)
    x = 3
    pass
