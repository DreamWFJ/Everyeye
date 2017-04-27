#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       role_views.py
CreateTime:     2017-04-04 20:11
"""
from app.core.db.sql.models import Role, User, Resource
from flask import render_template, request, url_for, flash, redirect
from . import manage_blueprint as manage

def get_user_list():
    return User.query.order_by(User.id)

def get_resource_list():
    return Resource.query.order_by(Resource.id)

@manage.route('/role', methods=['POST','GET'])
def role():
    if request.method == 'POST':
        print request.form
        name = request.form.get('name')
        role_status = request.form.get('role_status')
        role_status = True if role_status == "on" else False
        default_role = request.form.get('default_role')
        if Role.query.filter_by(name=name).first():
            flash("Error: role name repeat")
        else:
            Role.insert_roles(name, status=role_status, default=bool(default_role))
            flash("Success: add role ok")

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
                           current_url=url_for('manage.role'), user_list=get_user_list(), resource_list=get_resource_list(),
                           total=Role.query.count(), query_size=filter_result.count())


@manage.route('/role/edit-status')
def edit_role_status():
    print request.args
    flash('Edit "%s" status to "%s" success'%(request.args.get('role_id'), request.args.get('status')))
    return redirect(url_for('manage.role'))

@manage.route('/role/search', methods=['POST'])
def role_search():
    print request.form.get('content')
    return redirect(url_for('manage.role'))

@manage.route('/role/delete', methods=['POST'])
def delete_role():
    print request.form
    ids = request.form.get('ids')
    print ids.split(',')
    Role.delete_role_by_ids(ids.split(','))
    return "Delete ids '%s' success"%ids

@manage.route('/role/bind-user', methods=['POST'])
def bind_role_user():
    # print request.form
    role_name = request.form.get('name')
    user_ids = request.form.getlist('user_ids')
    Role.add_role_user_by_ids(role_name, user_ids)
    print "user_ids: ",user_ids
    flash('Bind role "%s" user id list "%s" success'%(role_name, user_ids))
    return redirect(url_for('manage.role'))

@manage.route('/role/bind-resource', methods=['POST'])
def bind_role_resource():
    print request.form
    role_name = request.form.get('name')
    resource_id = request.form.getlist('resource_id')
    Role.add_role_resource_by_id(role_name, resource_id)
    flash('Bind role "%s" resource id "%s" success'%(role_name, resource_id))
    return redirect(url_for('manage.role'))

@manage.route('/role/set-default')
def set_default_role():
    print request.args
    flash('Edit "%s" default role to "%s" success'%(request.args.get('role_id'), request.args.get('status')))
    return redirect(url_for('manage.role'))