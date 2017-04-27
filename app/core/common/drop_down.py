# -*- coding: utf-8 -*-
# ===================================
# ScriptName : drop_down.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-04-27 15:34
# ===================================

from app.core.db.sql.models import User, Role, Right, Resource

def get_role_list():
    return Role.query.order_by(Role.id)

def get_user_list():
    return User.query.order_by(User.id)

def get_resource_list():
    return Resource.query.order_by(Resource.id)

def get_right_list():
    return Right.query.order_by(Right.id)