# -*- coding: utf-8 -*-
# ===================================
# ScriptName : relationship_views.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-04-26 9:43
# ===================================
from app import sql_db
from app.core.db.sql.models import Role, User, ResourcesRights, RolesResources
from flask import render_template, redirect, request, url_for, flash
from . import manage_blueprint as manage

@manage.route('/user-role', methods=['POST','GET'])
def user_role():
    search_content = " 1=1 "
    content = request.args.get('content', '')
    if request.method == "POST":
        content = request.form.get('content')
        search_content = " users.name like '%{user_name}%' or roles.name like '%{role_name}%' " \
                         "or users.id like '%{user_id}%' ".format(user_name=content,
                                                                  role_name=content,
                                                                  user_id=content) if len(content) > 0 else " 1=1 "
    page = int(request.args.get('page', 1))
    page_size = request.args.get('page_size', 10)
    order_name = request.args.get('order_name', 'id')
    order_direction = request.args.get('order_direction', 'asc')
    if page_size == 'all':
        offset_size = page_size = None
    else:
        page_size = int(page_size)
        offset_size = (page - 1) * page_size

    role_id = request.args.get('role_id')
    if role_id:
        query_user_condition = " users.role_id = %s and roles.id = %s " %(role_id, role_id)
    else:
        query_user_condition = " users.role_id = roles.id "

    query_sql = 'select users.id as id, users.name as user_name, roles.name as role_name, ' \
                'users.create_at as create_at  from users, roles where %s and (%s) ' %(query_user_condition, search_content)

    paging_order_sql = " order by %s %s limit %s offset %s "%(order_name, order_direction, page_size, offset_size)

    query_size = len(list(sql_db.session.execute(query_sql)))
    result_sql = query_sql + paging_order_sql
    page_result = sql_db.session.execute(result_sql)

    return render_template('manage/admin/user_role_relationship.html', user_role_lists=page_result,
                           page_size=request.args.get('page_size', 10), page=request.args.get('page', 1),
                           current_url=url_for('manage.user_role'), query_size=query_size, search_content=content)

@manage.route('/user-role/delete', methods=['POST'])
def delete_user_role():
    print request.form
    ids = request.form.get('ids')
    print ids.split(',')
    User.delete_user_role_by_ids(ids.split(','))
    return "Delete ids '%s' success"%ids


@manage.route('/role-resource', methods=['POST','GET'])
def role_resource():
    search_content = " 1=1 "
    content = request.args.get('content', '')
    if request.method == "POST":
        content = request.form.get('content')
        print "content: ", content, type(content)
        search_content = " resources.name like '%{resource_name}%' or roles.name like '%{role_name}%' " \
                         "or roles_resources.id like '%{role_resource_id}%' ".format(resource_name=content,
                                                                                     role_name=content,
                                                                                     role_resource_id=content) if len(content) > 0 else " 1=1 "
    page = int(request.args.get('page', 1))
    page_size = request.args.get('page_size', 10)
    order_name = request.args.get('order_name', 'id')
    order_direction = request.args.get('order_direction', 'asc')

    role_id = request.args.get('role_id')
    if role_id:
        query_role_condition = " roles_resources.role_id = %s and roles.id = %s " %(role_id, role_id)
    else:
        query_role_condition = " roles_resources.role_id = roles.id "

    resource_id = request.args.get('resource_id')
    if resource_id:
        query_resource_condition = " roles_resources.resource_id = %s and resources.id = %s " %(resource_id, resource_id)
    else:
        query_resource_condition = " roles_resources.resource_id = resources.id "
    if page_size == 'all':
        offset_size = page_size = None
    else:
        page_size = int(page_size)
        offset_size = (page - 1) * page_size

    query_sql = 'select roles_resources.id as id, roles.name as role_name, resources.name as resource_name, ' \
                'roles_resources.right_weight as right_weight, roles_resources.create_at as create_at from roles, ' \
                'resources, roles_resources where %s and %s and (%s) ' %(query_role_condition, query_resource_condition, search_content)

    paging_order_sql = " order by %s %s limit %s offset %s "%(order_name, order_direction, page_size, offset_size)

    query_size = len(list(sql_db.session.execute(query_sql)))
    result_sql = query_sql + paging_order_sql
    page_result = sql_db.session.execute(result_sql)

    return render_template('manage/admin/role_resource_relationship.html', role_resource_lists=page_result,
                           page_size=request.args.get('page_size', 10), page=request.args.get('page', 1),
                           current_url=url_for('manage.role_resource'), query_size=query_size, search_content=content)

@manage.route('/role-resource/delete', methods=['POST'])
def delete_role_resource():
    print request.form
    ids = request.form.get('ids')
    print ids.split(',')
    RolesResources.delete_role_resource_by_ids(ids.split(','))
    return "Delete ids '%s' success"%ids


@manage.route('/resource-right', methods=['POST','GET'])
def resource_right():
    search_content = " 1=1 "
    content = request.args.get('content', '')
    if request.method == "POST":
        content = request.form.get('content')
        print "content: ", content, type(content)
        search_content = " resources.name like '%{resource_name}%' or rights.name like '%{right_name}%' " \
                         "or resources_rights.id like '%{resource_right_id}%' ".format(resource_name=content,
                                                                                       right_name=content,
                                                                                       resource_right_id=content) if len(content) > 0 else " 1=1 "

    page = int(request.args.get('page', 1))
    page_size = request.args.get('page_size', 10)
    order_name = request.args.get('order_name', 'id')
    order_direction = request.args.get('order_direction', 'asc')

    right_id = request.args.get('right_id')
    if right_id:
        query_right_condition = " resources_rights.right_id = %s and rights.id = %s " %(right_id, right_id)
    else:
        query_right_condition = " resources_rights.right_id = rights.id "

    resource_id = request.args.get('resource_id')
    if resource_id:
        query_resource_condition = " resources_rights.resource_id = %s and resources.id = %s " %(resource_id, resource_id)
    else:
        query_resource_condition = " resources_rights.resource_id = resources.id "
    if page_size == 'all':
        offset_size = page_size = None
    else:
        page_size = int(page_size)
        offset_size = (page - 1) * page_size

    query_sql = 'select resources_rights.id as id, resources.name as resource_name, rights.name as right_name, ' \
                'resources_rights.create_at as create_at from resources, rights, resources_rights ' \
                'where %s and %s and (%s) ' %(query_right_condition, query_resource_condition, search_content)

    paging_order_sql = " order by %s %s limit %s offset %s "%(order_name, order_direction, page_size, offset_size)

    query_size = len(list(sql_db.session.execute(query_sql)))
    result_sql = query_sql + paging_order_sql
    page_result = sql_db.session.execute(result_sql)

    return render_template('manage/admin/resource_right_relationship.html', resource_right_lists=page_result,
                           page_size=request.args.get('page_size', 10), page=request.args.get('page', 1),
                           current_url=url_for('manage.resource_right'), query_size=query_size, search_content=content)

@manage.route('/resource-right/delete', methods=['POST'])
def delete_resource_right():
    print request.form
    ids = request.form.get('ids')
    print ids.split(',')
    ResourcesRights.delete_resource_right_by_ids(ids.split(','))
    return "Delete ids '%s' success"%ids
