#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       role_views.py
CreateTime:     2017-04-04 20:11
"""
from app.core.db.sql.models import Role
from flask import render_template, request, url_for, flash
from . import manage_blueprint as manage

@manage.route('/role', methods=['POST','GET'])
def role():
    if request.method == 'POST':
        print request.form
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        repeat_password = request.form.get('repeat_password')
        if Role.query.filter_by(name=username).first():
            flash("Error: username repeat")
        elif Role.query.filter_by(email=email).first():
            flash("Error: email repeat")
        else:
            if password == repeat_password:
                Role.insert_users(username, email, password)
            else:
                flash("Error: differt password")
    page = int(request.args.get('page', 1))
    page_size = request.args.get('page_size', 10)
    order_name = request.args.get('order_name', 'id')
    order_direction = request.args.get('order_direction', 'asc')
    if page_size == 'all':
        offset_size = page_size = None
    else:
        page_size = int(page_size)
        offset_size = (page - 1) * page_size

    filter_result = Role.query.order_by(eval("Role.%s.%s()"%(order_name, order_direction)))
    page_result = filter_result.limit(page_size).offset(offset_size)
    return render_template('manage/admin/role.html', roles=page_result,
                           page_size=request.args.get('page_size', 10), page=request.args.get('page', 1),
                           current_url=url_for('manage.role'),
                           total=Role.query.count(), query_size=filter_result.count())