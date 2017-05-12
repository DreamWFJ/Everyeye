# -*- coding: utf-8 -*-
# ===================================
# ScriptName : user.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-08 9:49
# ===================================
from flask.views import MethodView
from flask import request
from flask import jsonify
from app.core.db.sql.models import User
from ..  import api_v1_blueprint as api

# REST API方法实现如下面格式
class UserAPI(MethodView):
    """
    URL	HTTP 方法	描述
    /users/	GET	获得全部用户的列表
    /users/	POST	创建一个新用户
    /users/<id>	GET	显示某个用户
    /users/<id>	PUT	更新某个用户
    /users/<id>	DELETE	删除某个用户
    """
    def get(self, user_id):
        if user_id is None:
            # 处理列表
            user_list = []
            users = User.query.all()
            for user in users:
                user_list.append(user.to_json())
            return jsonify({'status':True, 'result':user_list})
        else:
            # 处理单个用户
            user = User.query.get_or_404(user_id)
            return jsonify(user.to_json())

    def post(self):
        print request.form
        return jsonify({'status': True, 'msg':"post request"})

    def delete(self, user_id):
        # delete a single user
        print 'delete user: ', user_id
        return jsonify({'status': True})

    def put(self, user_id):
        # update a single user
        print 'update user: ', user_id
        return jsonify({'status': True, 'msg':"put request"})

# 注册路由
user_view = UserAPI.as_view('user_api')
api.add_url_rule('/users', defaults={'user_id': None}, view_func=user_view, methods=['GET',])
api.add_url_rule('/users', view_func=user_view, methods=['POST',])
api.add_url_rule('/users/<int:user_id>', view_func=user_view, methods=['GET', 'PUT', 'DELETE'])

# 多个类似API可以使用下面的方法
# def register_api(view, endpoint, url, pk='id', pk_type='int'):
#     view_func = view.as_view(endpoint)
#     app.add_url_rule(url, defaults={pk: None},
#                      view_func=view_func, methods=['GET',])
#     app.add_url_rule(url, view_func=view_func, methods=['POST',])
#     app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
#                      methods=['GET', 'PUT', 'DELETE'])
# register_api(UserAPI, 'user_api', '/users/', pk='user_id')