# -*- coding: utf-8 -*-
# ===================================
# ScriptName : __init__.py.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-04-05 9:59
# ===================================


from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views