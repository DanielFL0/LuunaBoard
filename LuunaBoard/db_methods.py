from werkzeug.utils import secure_filename
from LuunaBoard import db
from LuunaBoard.models import Category, Thread, Comment
from LuunaBoard.config import ALLOWED_EXTENSIONS
from sqlalchemy import asc, desc
import sys
import platform

def fetch_latest_threads(quantity):
    threads = Thread.query.order_by(Thread.date_posted).limit(quantity).all()
    return threads

def fetch_threads(board_category_id, quantity):
    # Don't like how this is looking
    threads = Thread.query
    threads = threads.filter_by(category_id=board_category_id)
    threads = threads.order_by(desc(Thread.date_posted)).limit(quantity).all()
    return threads

def fetch_categories():
    categories = Category.query.all()
    return categories

def fetch_category(category_id):
    category = Category.query.filter_by(id=category_id).first()
    return category

def fetch_thread(thread_id):
    thread = Thread.query.filter_by(id=thread_id).first()
    return thread

def fetch_comments(thread_id):
    comments = Comment.query.filter_by(thread_id=thread_id).all()
    return comments

def fetch_system_info():
    python_version = sys.version
    system = platform.system()
    operating_system = platform.platform()
    return python_version, "{}: {}".format(system, operating_system)

def create_thread(thread_title, thread_content, thread_image, thread_category_id):
    thread = Thread(title=thread_title, content=thread_content, image=thread_image, category_id=thread_category_id)
    db.session.add(thread)
    db.session.commit()

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
