# -*- coding: utf-8 -*-
# ===================================
# ScriptName : handle.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-05-09 10:31
# ===================================

import functools
from flask_login import current_user
from flask_socketio import disconnect

# 长连接必须登录才可以使用
def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped

# 下面是一个例子
# @socketio.on('my event')
# @authenticated_only
# def handle_my_custom_event(data):
#     emit('my response', {'message': '{0} has joined'.format(current_user.name)},
#          broadcast=True)