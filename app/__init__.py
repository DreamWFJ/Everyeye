# -*- coding: utf-8 -*-
# ===================================
# ScriptName : __init__.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-07 14:56
# ===================================
from flask import Flask, Blueprint
from config import config
from v1.routes import load_api_routes
def load_config(env):
    """加载配置类"""
    if env.startswith('p') or env.startswith('pr') or env.startswith('pro') or env == "production":
        e = "production"
    elif env.startswith('t') or env.startswith('te') or env.startswith('tes') or env == "test":
        e = "test"
    elif env.startswith('d') or env.startswith('de') or env.startswith('dev') or env == "development":
        e = "test"
    else:
        e = "default"
    return config[e]

def create_app(env=None):
    app = Flask(__name__)
    # 对REST API的支持
    load_api_routes(app)
    config = load_config(env)
    app.config.from_object(config)
    # 这下边要修改为视图的API蓝图
    # from .v1 import api as api_1_0_blueprint
    # app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')
    return app


if __name__ == '__main__':
    pass
    