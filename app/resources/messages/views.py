# -*- coding: utf-8 -*-
# ===================================
# ScriptName : views.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-04-06 17:26
# ===================================


from app import socketio
from flask import render_template
from .. import resource_blueprint as message
from app.core.db.sql.models import Message
from flask_login import login_required, current_user
from flask_socketio import emit, send
from app.core.auth.handle import authenticated_only

@socketio.on('message')
@authenticated_only
def handle_message(message):
    print('received message: ' + message)

@socketio.on('json')
@authenticated_only
def handle_json(json):
    print('received json: ' + str(json))

def ack():
    print 'message was received!'

# 支持回调
@socketio.on('my event')
@authenticated_only
def handle_my_custom_event(json):
    emit('my response', json, callback=ack)

# 支持广播
@socketio.on('my event')
@authenticated_only
def handle_my_custom_event(data):
    emit('my response', data, broadcast=True)

# 对房间的支持
from flask_socketio import join_room, leave_room

@socketio.on('join')
@authenticated_only
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', room=room)

@socketio.on('leave')
@authenticated_only
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)

# 测试连接和端口连接
@socketio.on('connect', namespace='/chat')
@authenticated_only
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/chat')
@authenticated_only
def test_disconnect():
    print('Client disconnected')

@message.route('/<string:username>/messaging/')
@login_required
def messaging(username):
    messages = Message.query.all()
    if messages is None:
        messages = []
    return render_template('resources/message/messaging.html', messages=messages)
    