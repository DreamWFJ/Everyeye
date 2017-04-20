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

@main.route('/<string:username>/action-log/')
@login_required
def action_log(username):
    return render_template('resources/log/action_log.html')
    