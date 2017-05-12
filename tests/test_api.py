#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       test_api.py
CreateTime:     2017-03-19 12:15
"""
import json
import unittest
from app import create_app
from base64 import b64encode
import flask_testing

# 测试json格式返回的API
# @app.route("/ajax/")
# def some_json():
#     return jsonify(success=True)

class TestViews(unittest.TestCase):
    def setUp(self):
        self.app = create_app('default')
        self.app_context = self.app.app_context()
        self.app_context.push()
        # db.create_all()
        # Role.insert_roles()
        self.client = self.app.test_client()

    def tearDown(self):
        # db.session.remove()
        # db.drop_all()
        self.app_context.pop()

    def get_api_headers(self, username, password):
        return {
            'Authorization':
                'Basic ' + b64encode(
                    (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_user_api_get(self):
        # response = self.client.post(
        #     url_for('api.new_post'),
        #     headers = self.get_api_headers('john@example.com', 'cat'),
        #     data = json.dumps({'body': 'body of the *blog* post'}))

        response = self.client.get("/api/v1.0/users", content_type = 'application/json')
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['status'] == True)