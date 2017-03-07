# -*- coding: utf-8 -*-
# ===================================
# ScriptName : __init__.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-07 14:56
# ===================================
from flask import Flask
from config import config
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
    config = load_config(env)
    app.config.from_object(config)
    # configure your app...
    return app


if __name__ == '__main__':
    pass
    