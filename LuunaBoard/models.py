from datetime import datetime
from LuunaBoard import db
from flask_sqlalchemy import SQLAlchemy

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<Category %r>" % self.name


class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=False, nullable=False)
    content = db.Column(db.String(200), unique=False, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    replies = db.Column(db.Integer, default=0)
    image = db.Column(db.String(100), nullable=False, default='default.jpg')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref='thread', lazy=True)
    comments = db.relationship('Comment', backref='thread', lazy=True)

    def __repr__(self):
        return "<Thread %r>" % self.title

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), unique=False, nullable=False)
    image = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)

    def __repr__(self):
        return "<Comment %r>" % self.content

db.create_all()
db.session.commit()