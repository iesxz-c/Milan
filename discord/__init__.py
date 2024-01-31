from flask import Flask, jsonify,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_socketio import SocketIO, join_room, leave_room, send
from flask_session import Session


db = SQLAlchemy()
DB_NAME = "database.db"
skt = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'akash'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SESSION_TYPE'] = 'filesystem'
    db.init_app(app)
    skt.init_app(app)
    Session(app)

    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)


    from .views import views
    from .auth import auth
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    from .models import User, Friend

    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
#this is telling flask how we loading a user
#it gonna look for the pk
    return app

def create_database(app):
    if not path.exists('discord/' + DB_NAME):
        db.create_all(app=app)
        print('Created')


