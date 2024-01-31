from flask import Blueprint,render_template, request, flash, jsonify,redirect,url_for,session
from flask_login import login_user, login_required, logout_user, current_user
from flask_socketio import join_room,leave_room ,SocketIO,send,emit
from . import db,skt
from .models import User, Friend

views = Blueprint('views', __name__)

@views.route('/home')
@views.route('/', methods = ['GET', 'POST'])
@login_required
def home():
    if request.method == "POST":
        friend_username = request.form.get("friend")

        # Check if the friend username exists
        friend = User.query.filter_by(username=friend_username).first()
        if friend is None:
            flash('Username does not exist.', category='error')
            return redirect(url_for('views.home'))

        # Check if the user is trying to add themselves
        if friend_username == current_user.username:
            flash('You cannot add yourself as a friend.', category='error')
            return redirect(url_for('views.home'))

        # Check if the friend is already added
        if Friend.query.filter_by(user_id=current_user.id, friend=friend_username).first():
            flash('Username already in your friends.', category='error')
            return redirect(url_for('views.home'))

        # Check if the reverse friend relationship already exists
        reverse_friend = Friend.query.filter_by(user_id=friend.id, friend=current_user.username).first()
        if reverse_friend:
            room = reverse_friend.room
        else:
            room = str(current_user.id) + str(friend.id)

        # Add the friend relationship
        new_friend = Friend(friend=friend_username, room=room, user_id=current_user.id)
        db.session.add(new_friend)
        db.session.commit()

        flash('Friend added successfully.', category='success')
        return redirect(url_for('views.home'))
    friends = Friend.query.filter_by(user_id=current_user.id).all()
    flist = [friend.friend for friend in friends]
    return render_template("home.html", user=current_user, username=current_user.username, flist=flist)

@skt.on('connect', namespace='/room')
def connect():
    username = session.get("user_id")
    print(f"Connected user: {username}")
    print("Session data:", session)
    print("Connected")


@skt.on('join_room', namespace='/room')
def joinroom(data):
    username = session.get("user_id")
    friend = data
    friend_entry = Friend.query.filter_by(user_id=username, friend=friend).first()

    if friend_entry:
        room = friend_entry.room
        session['room'] = room
        join_room(room)
        emit('activity', {'name': username, 'msg': "is online", 'room': room}, to=room)

@skt.on('disconnect', namespace='/room')
def leaveroom():
    username = session.get("user_id")
    room = session.get("room")

    if username and room:
        leave_room(room)
        emit('message', {"name": username, "msg": "is offline"}, to=room)
        print("Disconnected from room:", room)
    else:
        print("Disconnected without a username or room.")

@skt.on('sendmsg', namespace="/room")
def sendmsg(data):
    username = session.get("user_id")
    room = session.get("room")

    if username and room:
        msg = data
        content = {
            'name': username,
            'msg': msg
        }
        emit('message', content, to=room)
        print(msg)
    else:
        print("User or room information not available.")