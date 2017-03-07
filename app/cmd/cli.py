# -*- coding: utf-8 -*-
# ===================================
# ScriptName : cli.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-07 15:21
# ===================================
from flask_script.commands import ShowUrls, Clean
from flask_script import Command, Server, Option, prompt_bool

db = "从数据对象过来，需要统一一个方法"


class InitDB(Command):
    '''init database'''
    def __init__(self, default_name='Joe'):
        self.default_name=default_name

    def get_options(self):
        return [
            Option('-n', '--name', dest='name', default=self.default_name),
        ]

    def run(self, name):
        print "hello",  name

class DropDB(Command):
    '''drop all databases data'''
    def __init__(self, default_name='Joe'):
        self.default_name=default_name

    def get_options(self):
        return [
            Option('-n', '--name', dest='name', default=self.default_name),
        ]

    def run(self, name):
        if prompt_bool(
            "Are you sure you want to lose all your data"):
            db.drop_all()

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