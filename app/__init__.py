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
from flask_restful import Api
from app.core.resources.user import User


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
#
# def load_database_backend(app):
#     DB_BACKEND = app.config["DB_BACKEND"]
#     print "DB_BACKEND: ",DB_BACKEND
#     if DB_BACKEND == "sqlalchemy":
#         from flask_sqlalchemy import SQLAlchemy
#         from core.db.sqlalchemy import SQLAlchemyCommand
#         # from flask_migrate import Migrate, MigrateCommand
#         # from core.db.sqlalchemy import SQLAlchemyUserDatastore, User, Role
#         DB_CONNECT_HANDLER = SQLAlchemy(app)
#         # 只针对sqlalchemy 使用的数据转移，类似django中一样
#         # migrate = Migrate(app, DB_CONNECT_HANDLER)
#         # manager = Manager(app)
#         # manager.add_command('db', MigrateCommand)
#         app.config["DB_CONNECT_HANDLER"] = DB_CONNECT_HANDLER
#         app.config["DB_COMMAND"] = SQLAlchemyCommand()
#         # app.config["USER_STORAGE"] = SQLAlchemyUserDatastore(DB_CONNECT_HANDLER, User, Role)
#     elif DB_BACKEND == "pymongo":
#         from flask_pymongo import MongoClient
#     else:
#         # 这里使用sqlite3处理
#         pass
#     return app


def create_app(env=None):
    app = Flask(__name__)
    app.config.from_object(load_config(env))
    config_backend_database(app)
    EveryEyeApi(app)
    return app

def config_backend_database(app):
    pass

class EveryEyeApi(object):
    def __init__(self, app=None, prefix=None):
        self.app = app
        self.prefix = self._init_url_prefix(prefix)
        self.api = Api(self.app, self.prefix)
        if app is not None:
            self.init_api(app)


    def _init_url_prefix(self, prefix):
        if not prefix:
            prefix = '{prefix}/v{version}'.format(prefix=self.app.config['URL_PREFIX'],
                                                  version=self.app.config['URL_PREFIX'])
        return prefix


    def _get_state(self):
        for k, v in self.app.config.items():
            setattr(self, k.lower(), v)
        self.load_database_backend()

    def init_api(self, app):
        self.api.init_app(app)
        app.extensions['every_eye_api'] = self._get_state()

    def load_api_routes(self):
        self.api.add_resource(User, '/user', '/user/<int:user_id>', endpoint='user')

    def load_database_backend(self):
        DB_BACKEND = self.app.config["DB_BACKEND"]
        if DB_BACKEND == "sqlalchemy":
            from flask_sqlalchemy import SQLAlchemy
            db_handler = SQLAlchemy()
            self.app.config["DB_HANDLER"] = db_handler
            from app.core.db.sqlalchemy import SQLAlchemyUserDatastore
            from app.core.db.sqlalchemy import User as db_user
            from app.core.db.sqlalchemy import Role as db_role
            self.app.config["DB_USER_HANDLER"] = SQLAlchemyUserDatastore(db_handler, db_user, db_role)
            db_handler.init_app(self.app)
        elif DB_BACKEND == "pymongo":
            from flask_pymongo import MongoClient
        else:
            # 这里使用sqlite3处理
            pass