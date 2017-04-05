# -*- coding: utf-8 -*-
# ===================================
# ScriptName : views.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-04-05 10:42
# ===================================

from flask_login import login_required
from flask import render_template, abort
from .. import resource_blueprint as main
from app.core.db.sql.models import User, Log
from app.utils.decorators import permission_required

@main.route('/log/<name>')
@login_required
@permission_required('log', 'show')
def logs(name):
    user = User.query.filter_by(name=name).first()
    if user is None:
        abort(404)
    logs = Log.query.filter_by(user_id=user.id).all()
    if logs is None:
        abort(404)
    return render_template('resources/log/log.html', logs=logs)
    