from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from LuunaBoard.config import SECRET_KEY
from LuunaBoard.config import DB_CONNECTION
from LuunaBoard.config import MEDIA_FOLDER

app = Flask(__name__)
app.config['SECRET KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONNECTION
app.config['UPLOAD_FOLDER'] = MEDIA_FOLDER
db = SQLAlchemy(app)

import LuunaBoard.views