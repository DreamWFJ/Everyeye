# -*- coding: utf-8 -*-
# ===================================
# ScriptName : __init__.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-07 14:56
# ===================================
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail
from app.core.resources import urls
from config import Config

mail = Mail()
db = SQLAlchemy()

def create_app(env=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    migrate = Migrate(app, db)
    db.init_app(app)
    with app.test_request_context():
        db.create_all()
    return app


class EveryEyeApi(object):
    def __init__(self, app=None, prefix=None):
        self.app = app
        self.prefix = self._init_url_prefix(prefix)
        print self.prefix
        self.api = Api(self.app, self.prefix)
        if app is not None:
            self.init_api(app)


    def _init_url_prefix(self, prefix):
        if not prefix:
            prefix = '/{prefix}/v{version}'.format(prefix=self.app.config['URL_PREFIX'],
                                                  version=self.app.config['API_VERSION'])
        return prefix


    def _get_state(self):
        for k, v in self.app.config.items():
            setattr(self, k.lower(), v)
        self.load_database_backend()

    def init_api(self, app):
        self.api.init_app(app)
        self.load_api_routes()
        # app.extensions['every_eye_api'] = self._get_state()

    def load_api_routes(self):
        for url in urls:
            self.api.add_resource(url[0], url[1], endpoint=url[2])

    def load_database_backend(self):
        DB_BACKEND = self.app.config["DB_BACKEND"]
        if DB_BACKEND == "sqlalchemy":
            self.app.config["DB"] = SQLAlchemy(self.app)
        elif DB_BACKEND == "pymongo":
            pass
        else:
            # 这里使用sqlite3处理
            pass