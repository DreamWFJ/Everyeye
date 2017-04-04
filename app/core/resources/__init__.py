# -*- coding: utf-8 -*-
# ===================================
# ScriptName : __init__.py.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-08 19:54
# ===================================
from flask import Blueprint

main = Blueprint('main', __name__)
manage = Blueprint('manage', __name__)

from .frame import views as frame_views
from .manage import views as manage_views