# -*- coding: utf-8 -*-
# ===================================
# ScriptName : routes.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-08 19:37
# ===================================
from flask import Blueprint
from flask_restful import Api
from app.core.resources.user import User

def load_api_routes(app):
    api_blueprint = Blueprint('api', __name__, url_prefix='/api/v1.0')
    api = Api(api_blueprint)
    load_user_routes(api)
    app.register_blueprint(api_blueprint)


def load_user_routes(api):
    api.add_resource(User, '/User', '/User/<str:id>')

