from LuunaBoard import app
import os
from flask import request, url_for, render_template, redirect
from werkzeug.utils import secure_filename
from LuunaBoard import db
from LuunaBoard.models import Category, Thread, Comment
from LuunaBoard.config import MEDIA_FOLDER
from LuunaBoard.config import ALLOWED_EXTENSIONS

@app.route('/')
def home():
    threads = Thread.query.all()[-30:]
    return render_template('index.html', threads=threads)

@app.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)

def allowed_image(filename):
    extension = filename.split('.')[-1]
    if extension in ALLOWED_EXTENSIONS:
        return True
    return False

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
        if allowed_image(image.filename):
            create_thread(title, content, image.filename, category_result.id)
            image.save(os.path.join(MEDIA_FOLDER, secure_filename(image.filename)))
        else:
            create_thread(title, content, 'default.jpg', category_result.id)
        return redirect(url_for('board', category=category))
    return render_template('board.html', category=category_result, threads=threads)

def create_comment(comment_content, comment_image, comment_email, comment_thread_id):
    comment = Comment(content=comment_content, image=comment_image, email=comment_email, thread_id=comment_thread_id)
    db.session.add(comment)
    db.session.commit()

def update_reply_count(thread_id):
    comments = Comment.query.filter_by(thread_id=thread_id).all()
    comments_count = Comment.query.filter_by(thread_id=thread_id).count()
    thread_result = Thread.query.filter_by(id=thread_id).first()
    thread_result.replies = comments_count
    db.session.commit()

@app.route('/board/<int:category>/thread/<int:thread_id>', methods=['POST', 'GET'])
def thread(category, thread_id):
    category_result = Category.query.filter_by(id=category).first()
    thread_result = Thread.query.filter_by(id=thread_id).first()
    comments = Comment.query.filter_by(thread_id=thread_id).all()
    if request.method == 'POST':
        content = request.form['content']
        image = request.files['image']
        email = request.form['email']
        if allowed_image(image.filename):
            create_comment(content, image.filename, email, thread_result.id)
            image.save(os.path.join(MEDIA_FOLDER, secure_filename(image.filename)))  
        else:
            create_comment(content, 'default.jpg', email, thread_result.id)
        update_reply_count(thread_id)               
        return redirect(url_for('thread', category=category, thread_id=thread_id))
    return render_template('thread.html', category=category_result, thread=thread_result, comments=comments)

@app.route('/about')
def about():
    return render_template('about.html')
