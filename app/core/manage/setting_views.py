#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       setting_views.py
CreateTime:     2017-04-20 23:19
"""
from flask import render_template
from . import manage_blueprint as manage

@manage.route('/global-setting')
def global_setting():
    return render_template('manage/global_setting.html')