# -*- coding: utf-8 -*-
# ===================================
# ScriptName : views.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-04-06 17:26
# ===================================


from app import socketio
from .. import resource_blueprint as message
from app.core.db.sql.models import Message, User
from flask_login import login_required, current_user
from app.core.auth.handle import authenticated_only
from flask import render_template, render_template, session, request, url_for, jsonify
from flask_socketio import Namespace, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from sqlalchemy import and_

thread = None


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')


class MyNamespace(Namespace):
    @authenticated_only
    def on_my_event(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': message['data'], 'count': session['receive_count']})
    @authenticated_only
    def on_my_broadcast_event(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': message['data'], 'count': session['receive_count']},
             broadcast=True)
    @authenticated_only
    def on_join(self, message):
        join_room(message['room'])
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': 'In rooms: ' + ', '.join(rooms()),
              'count': session['receive_count']})
    @authenticated_only
    def on_leave(self, message):
        leave_room(message['room'])
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': 'In rooms: ' + ', '.join(rooms()),
              'count': session['receive_count']})
    @authenticated_only
    def on_close_room(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
                             'count': session['receive_count']},
             room=message['room'])
        close_room(message['room'])
    @authenticated_only
    def on_my_room_event(self, message):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': message['data'], 'count': session['receive_count']},
             room=message['room'])
    @authenticated_only
    def on_disconnect_request(self):
        session['receive_count'] = session.get('receive_count', 0) + 1
        emit('my_response',
             {'data': 'Disconnected!', 'count': session['receive_count']})
        disconnect()
    @authenticated_only
    def on_my_ping(self):
        emit('my_pong')
    @authenticated_only
    def on_connect(self):
        global thread
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
        emit('my_response', {'data': 'Connected', 'count': 0})
    @authenticated_only
    def on_disconnect(self):
        print('Client disconnected', request.sid)


# socketio.on_namespace(MyNamespace('/test'))

@message.route('/<string:user_id>/message-received')
@login_required
def message_received(user_id):
    page = int(request.args.get('page', 1))
    page_size = request.args.get('page_size', 10)
    order_name = request.args.get('order_name', 'id')
    order_direction = request.args.get('order_direction', 'asc')
    if page_size == 'all':
        offset_size = page_size = None
    else:
        page_size = int(page_size)
        offset_size = (page - 1) * page_size
    message_id = request.args.get('message_id')
    status = request.args.get('status')
    if status and status == '1':
        pass
        "需要设置消息状态为已读True"
    message_list = current_user.get_message_received(message_id=message_id)

    print "views message_list: ",message_list

    return render_template('resources/message/be_received.html', message_list=message_list,  async_mode= None,
                           page_size=request.args.get('page_size', 10), page=request.args.get('page', 1),
                           current_url=url_for('resource.message_received', user_id=current_user.id), query_size=10)

@message.route('/<string:user_id>/message-sent')
@login_required
def message_sent(user_id):
    page = int(request.args.get('page', 1))
    page_size = request.args.get('page_size', 10)
    order_name = request.args.get('order_name', 'id')
    order_direction = request.args.get('order_direction', 'asc')
    if page_size == 'all':
        offset_size = page_size = None
    else:
        page_size = int(page_size)
        offset_size = (page - 1) * page_size

    message_list = current_user.get_message_sent()
    print message_list
    if message_list is None:
        messages = []
    # else:
    #     print message.receivers
    return render_template('resources/message/be_sent.html', message_list=message_list,  async_mode= None,
                           page_size=request.args.get('page_size', 10), page=request.args.get('page', 1),
                           current_url=url_for('resource.message_received', user_id=current_user.id), query_size=10)

@message.route('/<string:user_id>/send-message', methods=['GET', 'POST'])
@login_required
def send_message(user_id):
    if request.method == 'POST':
        print request.form
        subject = request.form.get('subject')
        content = request.form.get('content')
        send_to_user_id = request.form.get('send_to')
        current_user.send_message(send_to_user_id, subject, content)
        return jsonify({'msg':"success"})
    page = int(request.args.get('page', 1))
    page_size = request.args.get('page_size', 10)
    order_name = request.args.get('order_name', 'id')
    order_direction = request.args.get('order_direction', 'asc')
    if page_size == 'all':
        offset_size = page_size = None
    else:
        page_size = int(page_size)
        offset_size = (page - 1) * page_size

    friend_list = User.query.limit(10).all()
    return render_template('resources/message/write_message.html', friend_list=friend_list,  async_mode= None,
                           page_size=request.args.get('page_size', 10), page=request.args.get('page', 1),
                           query_size=10)