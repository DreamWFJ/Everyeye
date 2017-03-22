# -*- coding: utf-8 -*-
# ===================================
# ScriptName : __init__.py.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-08 18:21
# ===================================

from .sqlalchemy import SQLAlchemyUserDatastore, User, Role, SqlalchemyBackend
from .mongodb import MongoBackend


class MySQLBackend(object):
    pass

_db_support = {
    "sqlalchemy":SqlalchemyBackend,
    "mysql":MySQLBackend,
    "mongo":MongoBackend
}

class DataStoreCommand(object):
    pass

class Database(object):
    def __init__(self, app, database=None):
        self.app = app
        self.database = database

        if self.database is None:
            self.load_database()

        self.register_handlers()

        self.Model = self.get_model_class()

    def load_database(self):
        self.database_config = dict(self.app.config['DATABASE'])

        self.database = self.database_class(self.database_name, **self.database_config)

    def get_model_class(self):
        pass

    def connect_db(self):
        self.database.connect()

    def close_db(self, exc):
        if not self.database.is_closed():
            self.database.close()

    def register_handlers(self):
        self.app.before_request(self.connect_db)
        self.app.teardown_request(self.close_db)


if __name__ == '__main__':
    pass
    