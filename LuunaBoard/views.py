from LuunaBoard import app
from flask import request, url_for

@app.route('/')
def home():
    return "You are at the home url {}".format(url_for('home'))

@app.route('/categories')
def categories():
    return "You are at the boards url {}".format(url_for('categories'))

@app.route('/board/<category>')
def board(category):
    return "You are at the board {}".format(category)

@app.route('/board/<category>/thread/<int:thread_id>')
def thread(category, thread_id):
    return "You are at the board {} watching the thread {}".format(category, thread_id)