# -*- coding: utf-8 -*-
# ===================================
# ScriptName : __init__.py.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-27 15:45
# ===================================

from flask import Blueprint

resource_blueprint = Blueprint('resource', __name__)
# 这个地方很奇怪，为什么必须导出来？，还有模板和静态文件的路径为什么是app目录下
from . import views
from .logs import views
from .persons import views
from .messages import views
from .comments import views
from .blogs import views