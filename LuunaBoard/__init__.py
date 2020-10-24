from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET KEY'] = 'njlanfdklaklfmdas'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:Franxx9208@localhost:3306/luunatest'
db = SQLAlchemy(app)

import LuunaBoard.views