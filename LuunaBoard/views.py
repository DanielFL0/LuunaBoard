from LuunaBoard import app
import os
from flask import request, url_for, render_template, redirect
from werkzeug.utils import secure_filename
from LuunaBoard import db
from LuunaBoard.models import Category, Thread, Comment
from LuunaBoard.config import MEDIA_FOLDER

@app.route('/')
def home():
    threads = Thread.query.all()[-30:]
    return render_template('index.html', threads=threads)

@app.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)

def create_thread(thread_title, thread_content, thread_image, thread_category_id):
    thread = Thread(title=thread_title, content=thread_content, image=thread_image, category_id=thread_category_id)
    db.session.add(thread)
    db.session.commit()

@app.route('/board/<int:category>', methods=['POST', 'GET'])
def board(category):
    category_result = Category.query.filter_by(id=category).first()
    threads = Thread.query.filter_by(category_id=category_result.id).all()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image = request.files['image']
        image.save(os.path.join(MEDIA_FOLDER, secure_filename(image.filename)))
        create_thread(title, content, image.filename, category_result.id)
        return redirect(url_for('board', category=category))
    return render_template('board.html', category=category_result, threads=threads)

@app.route('/board/<int:category>/thread/<int:thread_id>', methods=['POST', 'GET'])
def thread(category, thread_id):
    return "Test"

@app.route('/about')
def about():
    return render_template('about.html')
