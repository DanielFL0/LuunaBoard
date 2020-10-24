from LuunaBoard import app
from flask import request, url_for, render_template

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/categories')
def categories():
    return render_template('categories.html')

@app.route('/board/<category>')
def board(category):
    return render_template('index.html')

@app.route('/board/<category>/thread/<int:thread_id>')
def thread(category, thread_id):
    return render_template('about.html')