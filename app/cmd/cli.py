# -*- coding: utf-8 -*-
# ===================================
# ScriptName : cli.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-27 15:46
# Change     : Add clear session ----- will
# ===================================

import re
from flask_script.commands import ShowUrls, Clean
from flask_script import Command, Server
from flask_migrate import MigrateCommand, Migrate
from app import sql_db as _db
from app.core.db.sql.models import InitData


try:
    import simplejson as json
except ImportError:
    import json


def commit(fn):
    def wrapper(*args, **kwargs):
        fn(*args, **kwargs)
        _db.commit()
    return wrapper

def pprint(obj):
    print(json.dumps(obj, sort_keys=True, indent=4))




class InitDB(Command):
    '''init databases data'''
    def run(self, **kwargs):
        _db.drop_all()
        _db.create_all()
        InitData()
        print
        print('---------------- Database initialized successfully ------------------')
        print



class TestCommand(Command):
    """start unittest"""
    def run(self):
        import unittest
        tests = unittest.TestLoader().discover('tests')
        unittest.TextTestRunner(verbosity = 2).run(tests)

def init_command(manager, db):
    Migrate(manager.app, db)
    manager.add_option("-e", "--env",
                   dest="env",
                   help="set current environment, choice=[default, test, development, production]",
                   default="default",
                   required=False)
    manager.add_command("runserver", Server(host="0.0.0.0", port=8080))
    manager.add_command("urls", ShowUrls())
    manager.add_command("clean", Clean())
    manager.add_command("init", InitDB())
    manager.add_command('db', MigrateCommand)
    manager.add_command('test', TestCommand())

    return manager
    