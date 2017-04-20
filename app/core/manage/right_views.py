#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       right_views.py
CreateTime:     2017-04-04 20:11
"""

from flask import render_template
from . import manage_blueprint as manage

@manage.route('/right')
def right():
    return render_template('manage/admin/right.html')