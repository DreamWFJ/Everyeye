# -*- coding: utf-8 -*-
# ===================================
# ScriptName : __init__.py.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-04-05 9:59
# ===================================

from flask import Blueprint

manage_blueprint = Blueprint('manage', __name__)

from . import resource_views, role_views, right_views, user_views, article_views,log_views, message_views, relationship_views
    