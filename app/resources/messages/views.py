# -*- coding: utf-8 -*-
# ===================================
# ScriptName : views.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-04-06 17:26
# ===================================



from app import sql_db as db
from flask import render_template, flash,  redirect, url_for, abort
from .. import resource_blueprint as message
from app.core.db.sql.models import Message
from app.utils.decorators import permission_required
from flask_login import login_required, current_user

@message.route('/<string:username>/messaging/')
@login_required
def messaging(username):
    messages = Message.query.all()
    if messages is None:
        messages = []
    return render_template('resources/message/messaging.html', messages=messages)
    