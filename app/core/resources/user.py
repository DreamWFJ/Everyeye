# -*- coding: utf-8 -*-
# ===================================
# ScriptName : user.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-08 19:42
# ===================================
from flask import jsonify
from flask_restful import Resource

class User(Resource):
    def get(self, user_id=None):
        print user_id
        return jsonify({"user_id":user_id})

    def post(self):
        pass

if __name__ == '__main__':
    pass
    