#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       user_role_views.py
CreateTime:     2017-04-25 22:52
"""

from app.core.db.sql.models import Role, User
from flask import render_template, redirect, request, url_for, flash
from . import manage_blueprint as manage

@manage.route('/user-role', methods=['POST','GET'])
def user_role():
    page = int(request.args.get('page', 1))
    page_size = request.args.get('page_size', 10)
    order_name = request.args.get('order_name', 'id')
    order_direction = request.args.get('order_direction', 'asc')
    if page_size == 'all':
        offset_size = page_size = None
    else:
        page_size = int(page_size)
        offset_size = (page - 1) * page_size

    filter_result = Role.query.join(User).order_by(eval("Role.%s.%s()"%(order_name, order_direction)))
    print list(filter_result)
    page_result = filter_result.limit(page_size).offset(offset_size)
    return render_template('manage/admin/user_role_relationship.html', user_role_lists=page_result,
                           page_size=request.args.get('page_size', 10), page=request.args.get('page', 1),
                           current_url=url_for('manage.user_role'),
                           total=Role.query.count(), query_size=filter_result.count())




@manage.route('/user-role/delete', methods=['POST'])
def delete_user_role():
    print request.form
    ids = request.form.get('ids')
    print ids.split(',')
    User.delete_user_by_ids(ids.split(','))
    return "Delete ids '%s' success"%ids

@manage.route('/user-role/search', methods=['POST'])
def user_role_search():
    print request.form.get('content')
    return redirect(url_for('manage.user_role'))