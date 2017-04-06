# -*- coding: utf-8 -*-
# ===================================
# ScriptName : user.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-08 9:49
# ===================================
from flask.views import MethodView
from flask import request, app
from flask import jsonify
from app.core.db.sql.models import User

# REST API方法实现如下面格式
class UserApi(MethodView):
    def get(self, user_id):
        if user_id is None:
            # 处理列表
            user = {'test':'hjjsjs'}
            return jsonify(user.to_json())
        else:
            # 处理单个用户
            pass

    def post(self):
        user = User.from_form_data(request.form)

    def delete(self, user_id):
        # delete a single user
        pass

    def put(self, user_id):
        # update a single user
        pass

# 注册路由
# user_view = UserApi.as_view('user_api')
# app.add_url_rule('/users/', defaults={'user_id': None},
#                  view_func=user_view, methods=['GET',])
# app.add_url_rule('/users/', view_func=user_view, methods=['POST',])
# app.add_url_rule('/users/<int:user_id>', view_func=user_view,
#                  methods=['GET', 'PUT', 'DELETE'])

# 多个类似API可以使用下面的方法
# def register_api(view, endpoint, url, pk='id', pk_type='int'):
#     view_func = view.as_view(endpoint)
#     app.add_url_rule(url, defaults={pk: None},
#                      view_func=view_func, methods=['GET',])
#     app.add_url_rule(url, view_func=view_func, methods=['POST',])
#     app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
#                      methods=['GET', 'PUT', 'DELETE'])
#
# register_api(UserAPI, 'user_api', '/users/', pk='user_id')