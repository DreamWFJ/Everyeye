#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       example.py
CreateTime:     2017-03-19 10:49
"""
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)