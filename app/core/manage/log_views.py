#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       log_views.py
CreateTime:     2017-04-20 22:39
"""

from flask import render_template
from . import manage_blueprint as manage

@manage.route('/action-log')
def action_log():
    return render_template('manage/log/action_log.html')

@manage.route('/audit-log')
def audit_log():
    return render_template('manage/log/audit_log.html')