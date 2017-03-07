# -*- coding: utf-8 -*-
# ===================================
# ScriptName : __init__.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-07 14:56
# ===================================
from flask import Flask

def create_app(config=None):
    app = Flask(__name__)
    if config is not None:
        app.config.from_pyfile(config)
    # configure your app...
    return app


if __name__ == '__main__':
    pass
    