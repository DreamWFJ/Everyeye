# -*- coding: utf-8 -*-
# ===================================
# ScriptName : decorators.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-29 12:35
# ===================================

from functools import wraps
from flask import abort
from flask_login import current_user

def permission_required(resource, action):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.has_right(resource, action):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator