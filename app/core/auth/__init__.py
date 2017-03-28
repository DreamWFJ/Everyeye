# -*- coding: utf-8 -*-
# ===================================
# ScriptName : __init__.py.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-28 9:30
# ===================================

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
    