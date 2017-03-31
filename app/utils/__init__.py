# -*- coding: utf-8 -*-
# ===================================
# ScriptName : __init__.py.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-27 15:45
# ===================================


from uuid import uuid4
from datetime import datetime

def generate_uuid():
    return str(uuid4())


def get_current_0_24_time():
    now = datetime.now()
    zero_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
    twenty_four_time = now.replace(hour=23, minute=59, second=59, microsecond=999)
    return zero_time, twenty_four_time