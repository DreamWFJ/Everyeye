# -*- coding: utf-8 -*-
# ===================================
# ScriptName : __init__.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-07 14:56
# ===================================
from flask import Flask, g
from config import config
from v1.routes import load_api_routes
from v1.routes import EveryEyeApi

def load_config(env):
    """加载配置类"""
    if env.startswith('p') or env.startswith('pr') or env.startswith('pro') or env == "production":
        e = "production"
    elif env.startswith('t') or env.startswith('te') or env.startswith('tes') or env == "test":
        e = "test"
    elif env.startswith('d') or env.startswith('de') or env.startswith('dev') or env == "development":
        e = "development"
    else:
        e = "default"
    return config[e]

def load_database_backend(app):
    DB_BACKEND = app.config["DB_BACKEND"]
    print "DB_BACKEND: ",DB_BACKEND
    if DB_BACKEND == "sqlalchemy":
        from flask_sqlalchemy import SQLAlchemy
        from flask_migrate import Migrate, MigrateCommand
        from core.db.sqlalchemy import SQLAlchemyUserDatastore, User, Role
        DB_CONNECT_HANDLER = SQLAlchemy(app)
        # 只针对sqlalchemy 使用的数据转移，类似django中一样
        migrate = Migrate(app, DB_CONNECT_HANDLER)
        # manager = Manager(app)
        # manager.add_command('db', MigrateCommand)
        app.config["DB_CONNECT_HANDLER"] = DB_CONNECT_HANDLER
        app.config["USER_STORAGE"] = SQLAlchemyUserDatastore(DB_CONNECT_HANDLER, User, Role)
    elif DB_BACKEND == "pymongo":
        from flask_pymongo import MongoClient
    else:
        # 这里使用sqlite3处理
        pass
    return app


def create_app(env=None):
    app = Flask(__name__)
    # 对REST API的支持, 希望将EveryEyeApi做成一个flask扩展，直接通过init_app就能加载相关资源，初始化配置
    EveryEyeApi.init_route()
    # app.register_blueprint(api_v1_bp,
    #     url_prefix='{prefix}/v{version}'.format(
    #     prefix=app.config['URL_PREFIX'],
    #     version=API_VERSION_V1))
    app = load_api_routes(app)
    print "current env: ", env
    config = load_config(env)
    print config
    app.config.from_object(config)
    # 加载数据库
    app = load_database_backend(app)
    print g["DB_CONNECT_HANDLER"]
    # 这下边要修改为视图的API蓝图
    # from .v1 import api as api_1_0_blueprint
    # app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')
    return app

    