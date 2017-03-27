# -*- coding: utf-8 -*-
# ===================================
# ScriptName : cli.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-27 15:46
# ===================================

import re
from flask_script.commands import ShowUrls, Clean
from flask_script import Command, Server, Option, prompt_bool, Shell
from flask_migrate import MigrateCommand, Migrate
from app import sql_db as _db
from app.core.db.sql.models import User, Role, Right, Resource, InitData, Address, Log, AuditLog
from werkzeug.security import generate_password_hash
from flask import current_app

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
    option_list = (
        Option('-d', '--database', dest='database', default=None),
    )

    def run(self, **kwargs):
        _db.drop_all()
        _db.create_all()
        InitData()
        print('Database initialized successfully.')
        pprint(kwargs)

class DropDB(Command):
    '''drop all databases data'''
    option_list = (
        Option('-d', '--database', dest='database', default=None),
    )

    def run(self, **kwargs):
        if prompt_bool(
            "Are you sure you want to lose all your data"):
            _db.drop_all()
            print('Database initialized successfully.')
            pprint(kwargs)

class CreateUserCommand(Command):
    """Create a user"""

    option_list = (
        Option('-e', '--email', dest='email', default=None),
        Option('-p', '--password', dest='password', default=None),
        Option('-a', '--active', dest='active', default=''),
    )

    def run(self, **kwargs):
        # sanitize active input
        ai = re.sub(r'\s', '', str(kwargs['active']))
        kwargs['active'] = ai.lower() in ['', 'y', 'yes', '1', 'active']


        kwargs['password'] = generate_password_hash(kwargs['password'])
        _db.create_user(**kwargs)
        print('User created successfully.')
        kwargs['password'] = '****'
        pprint(kwargs)

class TestCommand(Command):
    """start unittest"""
    def run(self):
        import unittest
        tests = unittest.TestLoader().discover('tests')
        unittest.TextTestRunner(verbosity = 2).run(tests)

def init_command(manager, db):
    Migrate(manager.app, db)
    def make_shell_context():
        return dict(app = manager.app, db = db, User = User, Role = Role, Right = Right,
                    Resource=Resource, Address=Address, Log=Log, AuditLog=AuditLog)

    manager.add_option("-e", "--env",
                   dest="env",
                   help="set current environment, choice=[default, test, development, production]",
                   default="default",
                   required=False)
    manager.add_command("runserver", Server(host="0.0.0.0", port=8080))
    manager.add_command("urls", ShowUrls())
    manager.add_command("clean", Clean())
    manager.add_command("init", InitDB())
    manager.add_command("drop", DropDB())
    manager.add_command('db', MigrateCommand)
    manager.add_command('test', TestCommand())
    manager.add_command("shell", Shell(make_context = make_shell_context))

    return manager
    