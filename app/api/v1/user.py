# -*- coding: utf-8 -*-
# ===================================
# ScriptName : user.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-08 9:49
# ===================================
from . import api
from flask import jsonify

@api.route('/users/<int:id>')
def get_user(id):
    user = {'test':'hjjsjs'}
    return jsonify(user.to_json())

