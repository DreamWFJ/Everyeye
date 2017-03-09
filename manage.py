# -*- coding: utf-8 -*-
# ===================================
# ScriptName : manage.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-07 15:00
# ===================================

from flask_script import Manager
from app import create_app
from app.cmd.cli import init_command

manager = Manager(create_app)
manager = init_command(manager)

if __name__ == '__main__':
    manager.run()
    