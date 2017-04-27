# -*- coding: utf-8 -*-
# ===================================
# ScriptName : views.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-04-05 10:39
# ===================================
from datetime import datetime
from flask import render_template, request
from . import resource_blueprint as main


@main.route('/')
def index():
    ct = datetime.utcnow()
    return render_template('index.html', current_time=ct)

@main.route('/search', methods=['POST'])
def search():
    print request.form
    return render_template('search.html')

@main.route('/<string:username>/setting/')
def setting(username):
    return render_template('resources/setting.html')

@main.route('/<string:username>/profile')
def profile(username):
    return render_template('resources/profile.html')