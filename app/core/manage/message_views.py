#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       message_views.py
CreateTime:     2017-04-20 22:39
"""

from flask import render_template
from . import manage_blueprint as manage

@manage.route('/messaging')
def messaging():
    return render_template('manage/message/messaging.html')

@manage.route('/send-message')
def send_message():
    return render_template('manage/message/send_message.html')