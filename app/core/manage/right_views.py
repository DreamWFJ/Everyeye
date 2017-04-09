#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       right_views.py
CreateTime:     2017-04-04 20:11
"""
from app.core.db.sql.models import Right
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import manage_blueprint as manage

# @manage.route('/rights')
# def right():
#     rights = Right.query.all()
#     return render_template('manage/right.html', rights=rights)