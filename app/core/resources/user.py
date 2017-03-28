# -*- coding: utf-8 -*-
# ===================================
# ScriptName : user.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-08 19:42
# ===================================
from flask import jsonify, current_app
from flask_restful import Resource, reqparse, fields, marshal_with
from werkzeug.local import LocalProxy
from app.utils.verify import valid_email
from app.core.exceptions import ValidationError



# _db = LocalProxy(lambda: current_app.config['DB_CONNECT_HANDLER'])

def email(email_str):
    """ return True if email_str is a valid email """
    if valid_email(email):
        return True
    else:
        raise ValidationError("{} is not a valid email")


user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument(
    'email', dest='email',
    type=email, location='form',
    required=True, help='The user\'s email',
)
user_post_parser.add_argument(
    'password', dest='password',
    type=str, location='form',
    required=True, help='The user\'s password',
)


user_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'create_at': fields.DateTime,
    'last_active_at': fields.DateTime,
    'active': fields.Boolean,
    'description': fields.String,
    'links': fields.Url("user")
}


class User(Resource):
    # @marshal_with(user_fields)
    def get(self, user_id=None):
        print user_id
        users = {"haha":"lala"}
        return jsonify({"users":users})

    def post(self):
        pass

class Test(Resource):
    def get(self):
        users = {"haha":"lala"}
        return jsonify({"users":users})

    def post(self):
        pass

