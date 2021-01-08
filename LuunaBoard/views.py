from LuunaBoard import app
import os
from flask import request, url_for, render_template, redirect
from werkzeug.utils import secure_filename
from LuunaBoard import db
from LuunaBoard.models import Category, Thread, Comment
from LuunaBoard import db_methods
from LuunaBoard import utils

@app.errorhandler(404)
def error_404(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_500(e):
    return render_template('404.html'), 500

@app.route('/')
def home():
    threads = db_methods.fetch_latest_threads(30)
    return render_template('index.html', threads=threads)

@app.route('/categories')
def categories():
    categories = db_methods.fetch_categories()
    return render_template('categories.html', categories=categories)

@app.route('/board/<int:category_id>', methods=['POST', 'GET'])
def board(category_id):
    message = None
    category_result = db_methods.fetch_category(category_id)
    threads = db_methods.fetch_threads(category_result.id, 30)
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image = request.files['image']
        if len(title) > 50 or len(content) > 200:
            message = "ERROR: Character limit exceeded"
        else:
            if utils.allowed_image(image.filename):
                filename = secure_filename(image.filename)
                db_methods.create_thread(title, content, filename, category_result.id)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                db_methods.create_thread(title, content, 'default.jpg', category_result.id)
            return redirect(url_for('board', category_id=category_id))
    return render_template('board.html', category=category_result, threads=threads, message=message)

@app.route('/board/<int:category_id>/thread/<int:thread_id>', methods=['POST', 'GET'])
def thread(category_id, thread_id):
    message = None
    category_result = db_methods.fetch_category(category_id)
    thread_result = db_methods.fetch_thread(thread_id)
    comments = db_methods.fetch_comments(thread_id)
    if request.method == 'POST':
        content = request.form['content']
        image = request.files['image']
        email = request.form['email']
        if len(content) > 50 or len(content) > 200:
            message = "ERROR: Character limit exceeded"
        else:
            if utils.allowed_image(image.filename):
                filename = secure_filename(image.filename)
                db_methods.create_comment(content, filename, email, thread_result.id)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  
            else:
                db_methods.create_comment(content, 'default.jpg', email, thread_result.id)
            db_methods.update_reply_count(thread_id)               
        return redirect(url_for('thread', category_id=category_id, thread_id=thread_id))
    return render_template('thread.html', category=category_result, thread=thread_result, comments=comments, message=message)

@app.route('/board/<int:category_id>/archive')
def archive(category_id):
    category_result = db_methods.fetch_category(category_id)
    threads = db_methods.fetch_threads(category_result.id, 30)
    return render_template('archive.html', category=category_result, threads=threads)

@app.route('/about')
def about():
    python_version, operating_system = db_methods.fetch_system_info()
    return render_template('about.html', python_version=python_version, operating_system=operating_system)
