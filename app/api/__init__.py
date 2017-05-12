# -*- coding: utf-8 -*-
# ===================================
# ScriptName : __init__.py.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-27 15:45
# ===================================


from flask import Blueprint

api_v1_blueprint = Blueprint('v1', __name__)
from v1.user import UserAPI
