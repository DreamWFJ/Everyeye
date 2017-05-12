#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       category_views.py
CreateTime:     2017-05-03 20:16
"""

from app.core.db.sql.models import Article, ArticleCategory
from flask_login import login_required, current_user
from flask import render_template, request, url_for, current_app
from .. import resource_blueprint as main
from app import sql_db


@main.route('/<string:username>/category', methods=['POST','GET'])
@login_required
def category(username):
    # 文章目录管理
    if request.method == "POST":
        name = request.form.get("name")
        status = request.form.get("status")
        status = True if status == "on" else False
        ArticleCategory.insert_category(name, status)
        current_user.add_action_log('create', 'category', True,
                                    'create category: "%s", status: "%s". insert data success'%(name, status))

    page = int(request.args.get('page', 1))
    page_size = request.args.get('page_size', 10)
    order_name = request.args.get('order_name', 'id')
    order_direction = request.args.get('order_direction', 'asc')
    if page_size == 'all':
        offset_size = page_size = None
    else:
        page_size = int(page_size)
        offset_size = (page - 1) * page_size

    category_id = request.args.get('category_id')
    if category_id:
        filter_result = ArticleCategory.query.filter_by(id=category_id)
    else:
        filter_result = ArticleCategory.query
    order_result = filter_result.order_by(eval("ArticleCategory.%s.%s()"%(order_name, order_direction)))
    page_result = order_result.limit(page_size).offset(offset_size)
    return render_template('resources/blog/category.html', category_list=page_result,
                           page_size=request.args.get('page_size', 10), page=request.args.get('page', 1),
                           current_url=url_for('resource.category', username=current_user.name), query_size=order_result.count())


@main.route('/<string:username>/delete-category', methods=['POST'])
@login_required
def delete_category(username):
    # 文章目录管理
    ids = request.form.get('ids')
    Article.delete_article_by_ids(ids.split(','))
    current_user.add_action_log('delete', 'category', True, 'delete category ids: "%s". remove data success'%ids)
    print "user: %s delete category id: %s"%(username, ids)
    return "Delete ids '%s' success"%ids