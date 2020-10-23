from LuunaBoard import app
from flask import request, url_for

@app.route('/')
def home():
    return "You are at the home url {}".format(url_for('home'))

@app.route('/boards')
def categories():
    return "You are at the boards url {}".format(url_for('board'))

@app.route('/<category>')
def board(category):
    return "You are at the board {}, the url is: {}".format(category, url_for('board'))

@app.route('/<category>/<int:thread_id>')
def thread(category, thread_id):
    return "You are at the board {} watching the thread {}, the url is {}".format(category, thread_id, url_for('thread'))