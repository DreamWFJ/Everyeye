# -*- coding: utf-8 -*-
# ===================================
# ScriptName : __init__.py.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-08 18:21
# ===================================

from .db_sqlalchemy import SQLAlchemyUserDatastore, User, Role, SqlalchemyBackend
from .db_mongo import MongoBackend


class MySQLBackend(object):
    pass

_db_support = {
    "sqlalchemy":SqlalchemyBackend,
    "mysql":MySQLBackend,
    "mongo":MongoBackend
}

class StoreBackend(object):
    def __init__(self, app, database=None):
        self.app = app
        if self.database is None:
            self.load_database()

        self.register_handlers()


    def load_database(self):
        self.database_engine = dict(self.app.config['DATABASE_ENGINE'])
        self.database = _db_support[self.database_engine](self.app)

    def connect_db(self):
        self.database.connect()

    def close_db(self, exc):
        if not self.database.is_closed():
            self.database.close()

    def register_handlers(self):
        self.app.before_request(self.connect_db)
        self.app.teardown_request(self.close_db)