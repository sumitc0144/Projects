from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt #Password Hashing with Flask-Bcrypt

app=Flask(__name__)
app.config['SECRET_KEY']='a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)

from flaskblog import routes