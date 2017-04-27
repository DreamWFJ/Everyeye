#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       resource_views.py
CreateTime:     2017-04-04 20:12
"""
from app.core.db.sql.models import Resource
from flask import render_template, request, url_for, flash, redirect
from . import manage_blueprint as manage
from app.core.common.drop_down import get_right_list, get_role_list

@manage.route('/resource', methods=['POST','GET'])
def resource():
    if request.method == 'POST':
        print request.form
        name = request.form.get('name')
        weight = request.form.get('weight')
        status = request.form.get('status')
        status = True if status == "on" else False
        if Resource.query.filter_by(name=name).first():
            flash("Error: resource name repeat")
        else:
            Resource.insert_resources(name, weight, status)
    page = int(request.args.get('page', 1))
    page_size = request.args.get('page_size', 10)
    order_name = request.args.get('order_name', 'id')
    order_direction = request.args.get('order_direction', 'asc')
    if page_size == 'all':
        offset_size = page_size = None
    else:
        page_size = int(page_size)
        offset_size = (page - 1) * page_size

    filter_result = Resource.query.order_by(eval("Resource.%s.%s()"%(order_name, order_direction)))
    page_result = filter_result.limit(page_size).offset(offset_size)
    return render_template('manage/admin/resource.html', resources=page_result,
                           page_size=request.args.get('page_size', 10), page=request.args.get('page', 1),
                           current_url=url_for('manage.resource'), right_list = get_right_list(), role_list = get_role_list(),
                           total=Resource.query.count(), query_size=filter_result.count())

@manage.route('/resource/edit-status')
def edit_resource_status():
    print request.args
    resource_id = request.args.get('resource_id')
    status = request.args.get('status')
    Resource.set_status(resource_id, bool(int(status)))
    flash('Edit "%s" status to "%s" success'%(resource_id, status))
    return redirect(url_for('manage.resource'))


@manage.route('/resource/search', methods=['POST'])
def resource_search():
    print request.form.get('content')
    return redirect(url_for('manage.resource'))

@manage.route('/resource/delete', methods=['POST'])
def delete_resource():
    print request.form
    ids = request.form.get('ids')
    print ids.split(',')
    Resource.delete_resource_by_ids(ids.split(','))
    return "Delete ids '%s' success"%ids

@manage.route('/resource/bind-right', methods=['POST'])
def bind_resource_right():
    print request.form
    name = request.form.get('name')
    right_ids = request.form.getlist('right_ids')
    Resource.add_resource_right_by_ids(name, right_ids)
    flash('Bind resource "%s" right ids "%s" success'%(name, right_ids))
    return redirect(url_for('manage.resource'))

@manage.route('/resource/bind-role', methods=['POST'])
def bind_resource_role():
    print request.form
    name = request.form.get('name')
    role_ids = request.form.getlist('role_ids')
    right_weight = request.form.get('right_weight')
    Resource.add_resource_role_by_ids(name, role_ids, right_weight)
    flash('Bind resource "%s" role "%s" success'%(name, role_ids))
    return redirect(url_for('manage.resource'))