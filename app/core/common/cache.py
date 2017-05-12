# -*- coding: utf-8 -*-
# ===================================
# ScriptName : cache.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-05-12 16:56
# ===================================
import json
from app import redis_store

def has_role_resource_right(role_id):
    if redis_store.hexists('role_resource_right', role_id):
        return True
    return False

def get_role_resource_right_weight(role_id, resource):
    role_resource_right = redis_store.hget('role_resource_right', role_id)
    # 这里出现了 ValueError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
    role_resource_right = json.loads(role_resource_right.replace('u', '').replace("'", '"'), "UTF-8")
    return role_resource_right[resource] if resource in role_resource_right else 0