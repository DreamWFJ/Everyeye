#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       user_views.py
CreateTime:     2017-04-04 20:11
"""

from app.core.db.sql.models import User
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import manage_blueprint as manage

@manage.route('/user')
def user():
    users = User.query.all()
    return render_template('manage/admin/user.html', users=users)

@manage.route('/test')
def test():
    return render_template('manage/test.html')

@manage.route('/frame')
def frame():
    return render_template('manage/frame.html')

@manage.route('/profile')
def profile():
    return render_template('manage/admin/profile.html')



@manage.route('/blog')
def blog():
    return render_template('manage/blog.html')

