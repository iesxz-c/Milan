from . import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)  # Increase the length as needed
    name = db.Column(db.String(50))  # Adjust the length as needed
    email = db.Column(db.String(120), unique=True, nullable=False)

class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    friend = db.Column(db.String(20), nullable=False)
    room = db.Column(db.String(50), nullable=False)

