#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       resource_views.py
CreateTime:     2017-04-04 20:12
"""

from app.core.db.sql.models import Resource
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import manage_blueprint as manage

# @manage.route('/resources')
# def resource():
#     resources = Resource.query.all()
#     return render_template('manage/resource.html', resources=resources)