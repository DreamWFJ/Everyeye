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
    if request.method == "POST":
        content = request.form.get('content')
        print "content: ", content, type(content)
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
    page_result = sql_db.session.execute('select users.id as id, users.name as user_name, roles.name as role_name, '
                                         'users.create_at as create_at  from users, roles where users.role_id = roles.id '
                                         'and (%s) order by %s %s limit %s offset %s'%(search_content, order_name,
                                                                                       order_direction, page_size, offset_size))
    return render_template('manage/admin/user_role_relationship.html', user_role_lists=page_result,
                           page_size=request.args.get('page_size', 10), page=request.args.get('page', 1),
                           current_url=url_for('manage.user_role'),
                           total=Role.query.count(), query_size=10)

@manage.route('/user-role/delete', methods=['POST'])
def delete_user_role():
    print request.form
    ids = request.form.get('ids')
    print ids.split(',')
    User.delete_user_role_by_ids(ids.split(','))
    return "Delete ids '%s' success"%ids

@manage.route('/user-role/search', methods=['POST'])
def user_role_search():
    print request.form.get('content')
    return redirect(url_for('manage.user_role'))

@manage.route('/role-resource', methods=['POST','GET'])
def role_resource():
    search_content = " 1=1 "
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
    if page_size == 'all':
        offset_size = page_size = None
    else:
        page_size = int(page_size)
        offset_size = (page - 1) * page_size

    page_result = sql_db.session.execute('select roles_resources.id as id, roles.name as role_name, resources.name as resource_name, '
                                         'roles_resources.right_weight as right_weight, roles_resources.create_at as create_at  '
                                         'from roles, resources, roles_resources where roles.id = roles_resources.role_id and '
                                         'resources.id = roles_resources.resource_id and (%s) order by %s %s '
                                         'limit %s offset %s'%(search_content, order_name, order_direction, page_size, offset_size))
    return render_template('manage/admin/role_resource_relationship.html', role_resource_lists=page_result,
                           page_size=request.args.get('page_size', 10), page=request.args.get('page', 1),
                           current_url=url_for('manage.role_resource'),
                           total=Role.query.count(), query_size=10)

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
    if request.method == "POST":
        content = request.form.get('content')
        print "content: ", content, type(content)
        search_content = " resources.name like '%{resource_name}%' or rights.name like '%{right_name}%' " \
                         "or resources_rights.id like '%{resource_right_id}%' ".format(resource_name=content,
                                                                                       right_name=content,
                                                                                       resource_right_id=content) if len(content) > 0 else " 1=1 "

    print "search_content: ",search_content
    page = int(request.args.get('page', 1))
    page_size = request.args.get('page_size', 10)
    order_name = request.args.get('order_name', 'id')
    order_direction = request.args.get('order_direction', 'asc')
    if page_size == 'all':
        offset_size = page_size = None
    else:
        page_size = int(page_size)
        offset_size = (page - 1) * page_size
    page_result = sql_db.session.execute('select resources_rights.id as id, resources.name as resource_name, '
                                         'rights.name as right_name, resources_rights.create_at as create_at  '
                                         'from resources, rights, resources_rights where rights.id = resources_rights.right_id '
                                         'and resources.id = resources_rights.resource_id and (%s) order by %s %s '
                                         'limit %s offset %s'%(search_content, order_name, order_direction, page_size, offset_size))

    return render_template('manage/admin/resource_right_relationship.html', resource_right_lists=page_result,
                           page_size=request.args.get('page_size', 10), page=request.args.get('page', 1),
                           current_url=url_for('manage.resource_right'),
                           total=Role.query.count(), query_size=10)

@manage.route('/resource-right/delete', methods=['POST'])
def delete_resource_right():
    print request.form
    ids = request.form.get('ids')
    print ids.split(',')
    ResourcesRights.delete_resource_right_by_ids(ids.split(','))
    return "Delete ids '%s' success"%ids
