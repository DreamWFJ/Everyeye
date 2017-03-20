# -*- coding: utf-8 -*-
# ===================================
# ScriptName : cli.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-07 15:21
# ===================================
import re
from flask_script.commands import ShowUrls, Clean
from flask_script import Command, Server, Option, prompt_bool
from flask import current_app
from werkzeug.local import LocalProxy

try:
    import simplejson as json
except ImportError:
    import json

_db = LocalProxy(lambda: current_app.config['DB_COMMAND'])

encrypt_password = ""
def pprint(obj):
    print(json.dumps(obj, sort_keys=True, indent=4))


def commit(fn):
    def wrapper(*args, **kwargs):
        fn(*args, **kwargs)
        _db.commit()
    return wrapper


class InitDB(Command):
    '''init databases data'''
    option_list = (
        Option('-d', '--database', dest='database', default=None),
    )

    @commit
    def run(self, **kwargs):
        _db.init_database(**kwargs)
        print('Database initialized successfully.')
        pprint(kwargs)

class DropDB(Command):
    '''drop all databases data'''
    option_list = (
        Option('-d', '--database', dest='database', default=None),
    )

    @commit
    def run(self, **kwargs):
        if prompt_bool(
            "Are you sure you want to lose all your data"):
            _db.drop_database(**kwargs)
            print('Database initialized successfully.')
            pprint(kwargs)

class CreateUserCommand(Command):
    """Create a user"""

    option_list = (
        Option('-e', '--email', dest='email', default=None),
        Option('-p', '--password', dest='password', default=None),
        Option('-a', '--active', dest='active', default=''),
    )

    @commit
    def run(self, **kwargs):
        # sanitize active input
        ai = re.sub(r'\s', '', str(kwargs['active']))
        kwargs['active'] = ai.lower() in ['', 'y', 'yes', '1', 'active']


        kwargs['password'] = encrypt_password(kwargs['password'])
        _db.create_user(**kwargs)
        print('User created successfully.')
        kwargs['password'] = '****'
        pprint(kwargs)


def init_command(manager):
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
    return manager