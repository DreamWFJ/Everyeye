# -*- coding: utf-8 -*-
# ===================================
# ScriptName : views.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-30 9:11
# ===================================

import os
from .. import main
from datetime import datetime
from flask_login import login_required
from flask import render_template, abort, redirect, url_for, current_app
from app.core.db.sql.models import User
from app.utils.decorators import permission_required
from werkzeug.utils import secure_filename
from .forms import PhotoForm

@main.route('/upload', methods=['GET', 'POST'])
def upload():
    form = PhotoForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            current_app.instance_path, 'photos', filename
        ))
        return redirect(url_for('index'))

    return render_template('upload.html', form=form)

@main.route('/')
def index():
    ct = datetime.utcnow()
    print ct
    return render_template('index.html', current_time=ct)

# 在模板中添加权限变量
@main.app_context_processor
def inject_permissions():
    return dict()

@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(name=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)

@main.route('/user')
@login_required
@permission_required('user', 'show')
def show_user():
    return 'has permission to show user'

@main.route('/log')
@login_required
@permission_required('log', 'update')
def write_log():
    return 'has permission to write log'