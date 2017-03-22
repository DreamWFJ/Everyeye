# -*- coding: utf-8 -*-
# ===================================
# ScriptName : __init__.py.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-08 19:54
# ===================================
from user import User, Test
urls = [
    [User, '/user', 'user'],
    [Test, '/test/<int:user_id>', 'test']
]