#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       resource_views.py
CreateTime:     2017-04-04 20:12
"""
from flask import render_template
from . import manage_blueprint as manage

@manage.route('/resource')
def resource():
    return render_template('manage/admin/resource.html')