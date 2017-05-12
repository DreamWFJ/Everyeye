#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       source_views.py
CreateTime:     2017-05-03 20:18
"""

from app.core.db.sql.models import ArticleSource
from flask_login import login_required, current_user
from flask import render_template, request, url_for, current_app
from .. import resource_blueprint as main



@main.route('/<string:username>/source', methods=['GET', 'POST'])
@login_required
def source(username):
    # 文章来源管理
    if request.method == "POST":
        name = request.form.get("name")
        status = request.form.get("status")
        status = True if status == "on" else False
        ArticleSource.insert_source(name, status)
        current_user.add_action_log('create', 'source', True,
                                    'create source: "%s", status: "%s". insert data success'%(name, status))
    page = int(request.args.get('page', 1))
    page_size = request.args.get('page_size', 10)
    order_name = request.args.get('order_name', 'id')
    order_direction = request.args.get('order_direction', 'asc')
    if page_size == 'all':
        offset_size = page_size = None
    else:
        page_size = int(page_size)
        offset_size = (page - 1) * page_size
    source_id = request.args.get('source_id')
    if source_id:
        filter_result = ArticleSource.query.filter_by(id=source_id)
    else:
        filter_result = ArticleSource.query
    order_result = filter_result.order_by(eval("ArticleSource.%s.%s()"%(order_name, order_direction)))
    page_result = order_result.limit(page_size).offset(offset_size)
    return render_template('resources/blog/source.html', source_list=page_result,
                           page_size=request.args.get('page_size', 10), page=request.args.get('page', 1),
                           current_url=url_for('resource.category', username=current_user.name), query_size=order_result.count())

@main.route('/<string:username>/delete-source', methods=['POST'])
@login_required
def delete_source(username):
    # 删除来源
    ids = request.form.get('ids')
    print ids.split(',')
    # ArticleKeyword.delete_keyword_by_ids(ids.split(','))
    print "user: %s delete source id: %s"%(username, ids)
    current_user.add_action_log('delete', 'source', True, 'delete source ids: "%s". remove data success'%ids)
    return "Delete ids '%s' success"%ids