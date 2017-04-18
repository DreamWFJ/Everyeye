# -*- coding: utf-8 -*-
# ===================================
# ScriptName : views.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-04-18 8:48
# ===================================


from flask_login import login_required
from flask import render_template, abort
from .. import resource_blueprint as main
from app.core.db.sql.models import User, Log
from app.utils.decorators import permission_required

# 请求形式为：https://127.0.0.1:8080/admin/comment
@main.route('/<string:user>/comment')
@login_required
def comment(user):
    print 'current request user: %s'%user
    return render_template('resources/comment/comment.html')