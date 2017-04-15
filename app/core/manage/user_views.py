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
    return render_template('manage/user.html', users=users)

@manage.route('/role')
def role():
    return render_template('manage/role.html')

@manage.route('/right')
def right():
    return render_template('manage/right.html')

@manage.route('/resource')
def resource():
    return render_template('manage/resource.html')

@manage.route('/log')
def log():
    return render_template('manage/log.html')

@manage.route('/test')
def test():
    return render_template('manage/test.html')

@manage.route('/test1')
def test1():
    return render_template('manage/test1.html')

@manage.route('/frame')
def frame():
    return render_template('manage/frame.html')\

@manage.route('/profile')
def profile():
    return render_template('manage/profile.html')

@manage.route('/user-profile')
def user_profile():
    return render_template('manage/user_profile.html')\

@manage.route('/email')
def email():
    return render_template('manage/email.html')

@manage.route('/audit-log')
def audit_log():
    return render_template('manage/audit_log.html')


@manage.route('/blog')
def blog():
    return render_template('manage/blog.html')

@manage.route('/comment')
def comment():
    return render_template('manage/comment.html')

@manage.route('/language-rule')
def language_rule():
    return render_template('manage/language_rule.html')