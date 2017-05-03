#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       keyword_views.py
CreateTime:     2017-05-03 20:17
"""

import os
from uuid import uuid4
import markdown
import random
from config import upload_image_path
from app.core.db.sql.models import Article, ArticleCategory, ArticleComment, ArticleKeyword, \
    User, ArticleSource
from flask_login import login_required, current_user
from flask import render_template, request, redirect, url_for, send_from_directory, current_app
from .. import resource_blueprint as main
from app import sql_db
from ..common import get_user_article_categorys, get_user_article_keywords, get_user_article_sources

@main.route('/<string:username>/keyword', methods=['POST','GET'])
@login_required
def keyword(username):
    # 关键词管理
    if request.method == "POST":
        name = request.form.get("name")
        color = request.form.get("color")
        status = request.form.get("status")
        status = True if status == "on" else False
        color_dict = {
            "1":"default",
            "2":"primary",
            "3":"success",
            "4":"info",
            "5":"warning",
            "6":"danger"
        }
        ArticleKeyword.insert_keyword(name, color_dict[str(color)], status)
    page = int(request.args.get('page', 1))
    page_size = request.args.get('page_size', 10)
    order_name = request.args.get('order_name', 'id')
    order_direction = request.args.get('order_direction', 'asc')
    if page_size == 'all':
        offset_size = page_size = None
    else:
        page_size = int(page_size)
        offset_size = (page - 1) * page_size

    article_id = request.args.get('article_id')
    if article_id:
        filter_sql = "select article_keyword.*, (select count(*) from articles,article_keywords where " \
                     "article_keywords.keyword_id = article_keyword.id and articles.id = {article_id} and " \
                     "article_keywords.article_id = {article_id}) as article_count from article_keyword,article_keywords, " \
                     "articles WHERE article_keywords.keyword_id = article_keyword.id and articles.id = {article_id} " \
                     "and article_keywords.article_id = {article_id} ".format(article_id=article_id)
    else:
        filter_sql = "select article_keyword.*, (select count(*) from articles,article_keywords where " \
                     "article_keywords.keyword_id = article_keyword.id and articles.id = article_keywords.article_id) as " \
                     "article_count from article_keyword"
    result_sql = filter_sql
    page_result = sql_db.session.execute(result_sql)

    return render_template('resources/blog/keyword.html', keyword_list=page_result,
                           page_size=request.args.get('page_size', 10), page=request.args.get('page', 1),
                           current_url=url_for('resource.keyword', username=current_user.name), query_size=10)

@main.route('/<string:username>/delete-keyword', methods=['POST'])
@login_required
def delete_keyword(username):
    # 文章目录管理
    ids = request.form.get('ids')
    print ids.split(',')
    ArticleKeyword.delete_keyword_by_ids(ids.split(','))
    print "user: %s delete article id: %s"%(username, ids)
    return "Delete ids '%s' success"%ids