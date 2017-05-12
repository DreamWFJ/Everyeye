#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       keyword_views.py
CreateTime:     2017-05-03 20:17
"""
from app.core.db.sql.models import User, ArticleKeywords, Keyword
from flask_login import login_required, current_user
from flask import render_template, request, redirect, url_for, current_app
from .. import resource_blueprint as main

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
        Keyword.insert_keyword(name, color_dict[str(color)], status)
        current_user.add_action_log('create', 'keyword', True,
                                    'create keyword: "%s", color: "%s", status: "%s". insert data success'%(name, color, status))

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
        # 多对多的查询：过滤条件为中间表，再到过滤对象表，最后得到结果
        filter_result = Keyword.query.filter(Keyword.articles.any(ArticleKeywords.article_id == article_id))
    else:
        filter_result = Keyword.query
    order_result = filter_result.order_by(eval("Keyword.%s.%s()"%(order_name, order_direction)))
    page_result = order_result.limit(page_size).offset(offset_size)

    # if article_id:
    #     filter_sql = "select article_keyword.*, (select count(*) from articles,article_keywords where " \
    #                  "article_keywords.keyword_id = article_keyword.id and articles.id = {article_id} and " \
    #                  "article_keywords.article_id = {article_id}) as article_count from article_keyword,article_keywords, " \
    #                  "articles WHERE article_keywords.keyword_id = article_keyword.id and articles.id = {article_id} " \
    #                  "and article_keywords.article_id = {article_id} ".format(article_id=article_id)
    # else:
    #     filter_sql = "select article_keyword.*, (select count(*) from articles,article_keywords where " \
    #                  "article_keywords.keyword_id = article_keyword.id and articles.id = article_keywords.article_id) as " \
    #                  "article_count from article_keyword"
    # result_sql = filter_sql
    # page_result = sql_db.session.execute(result_sql)

    return render_template('resources/blog/keyword.html', keyword_list=page_result,
                           page_size=request.args.get('page_size', 10), page=request.args.get('page', 1),
                           current_url=url_for('resource.keyword', username=current_user.name), query_size=order_result.count())

@main.route('/<string:username>/delete-keyword', methods=['POST'])
@login_required
def delete_keyword(username):
    # 文章目录管理
    ids = request.form.get('ids')
    Keyword.delete_keyword_by_ids(ids.split(','))
    current_user.add_action_log('delete', 'keyword', True, 'delete keyword ids: "%s". remove data success'%ids)
    print "user: %s delete article id: %s"%(username, ids)
    return "Delete ids '%s' success"%ids