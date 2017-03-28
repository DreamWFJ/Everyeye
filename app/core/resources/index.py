# -*- coding: utf-8 -*-
# ===================================
# ScriptName : index.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-28 10:56
# ===================================

from . import main
from datetime import datetime
from flask import render_template
@main.route('/')
def index():
    ct = datetime.utcnow()
    print ct
    return render_template('index.html', current_time=ct)
    