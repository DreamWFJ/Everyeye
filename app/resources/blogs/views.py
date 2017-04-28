#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       views.py
CreateTime:     2017-04-15 16:17
"""

from flask_login import login_required, current_user
from flask import render_template, request, redirect, url_for
from .. import resource_blueprint as main
from ..common import get_user_article_categorys, get_user_article_keywords, get_user_article_sources

@main.route('/<string:username>')
@login_required
def user_index(username):
    # 用户主页，这里展示文章简介
    print "show_user: ", username
    return render_template('resources/blog/index.html')

@main.route('/<string:username>/article')
@login_required
def article(username):
    # 文章列表
    article_list = [
        {
            'id':1,
            'title':"Test Article Title",
            'status':True,# 表示是否显示
            'view_count':16,
            'comment_count':12,
            'permit_comment':True,# 表示是否允许评论
            'public_time':"2010-12-25 12:31:45",
            'last_change_time':"2010-12-25 12:31:45",
            'last_view_time':"2010-12-25 14:12:01",
            'last_comment_time':"2010-12-25 14:12:43",
        },
        {
            'id':2,
            'title':"Test Article Title 2",
            'status':True,# 表示是否显示
            'view_count':24,
            'comment_count':14,
            'permit_comment':False,# 表示是否允许评论
            'public_time':"2010-12-25 12:31:45",
            'last_change_time':"2010-12-25 12:31:45",
            'last_view_time':"2010-12-25 14:12:01",
            'last_comment_time':"2010-12-25 14:12:43",
        },
        {
            'id':3,
            'title':"Test Article Title 2",
            'status':False,# 表示是否显示
            'view_count':15,
            'comment_count':14,
            'permit_comment':False,# 表示是否允许评论
            'public_time':"2010-12-25 12:31:45",
            'last_change_time':"2010-12-25 12:31:45",
            'last_view_time':"2010-12-25 14:12:01",
            'last_comment_time':"2010-12-25 14:12:43",
        }
    ]
    page = int(request.args.get('page', 1))
    page_size = request.args.get('page_size', 10)
    order_name = request.args.get('order_name', 'id')
    order_direction = request.args.get('order_direction', 'asc')
    if page_size == 'all':
        offset_size = page_size = None
    else:
        page_size = int(page_size)
        offset_size = (page - 1) * page_size
    return render_template('resources/blog/article.html', article_list=article_list,
                           page_size=request.args.get('page_size', 10), page=request.args.get('page', 1),
                           current_url=url_for('manage.user'), query_size=10)

# @main.route('/<string:username>/article/<uuid:article_id>')
@main.route('/<string:username>/article/<int:article_id>')
@login_required
def one_article(username, article_id):
    # 某一篇文章
    print "request article id: <%s>"%id
    return render_template('resources/blog/one_article.html')

@main.route('/<string:username>/new-article', methods=['POST','GET'])
@login_required
def new_article(username):
    # 写文章
    if request.method == 'GET':
        return render_template('resources/blog/new_article.html', article_categorys=get_user_article_categorys(),
                               article_keywords=get_user_article_keywords(), article_sources=get_user_article_sources())
    elif request.method == 'POST':
        print request.form
        title = request.form.get('title')
        category_id = request.form.get('category_id')
        source_id = request.form.get('source_id')
        keywords = request.form.get('keywords')
        enable_comment = request.form.get('enable_comment')
        content = request.form.get('summernote_content')
        content_type = "summernote"
        if len(content) == 0:
            content = request.form.get('markdown_content')
            content_type = "markdown"
        reference_links = request.form.getlist('reference_links_box[]')
        print "title : ",title
        print "category_id : ",category_id
        print "source_id : ",source_id
        print "keywords : ",keywords
        print "enable_comment : ",enable_comment
        print "content : ",content
        print "content_type : ",content_type
        print "reference_links : ",reference_links
        print "current_user_id : ",current_user.id
        return redirect(url_for('resource.article', username=current_user.name))

@main.route('/<string:username>/delete-article')
@login_required
def delete_article(username):
    # 文章目录管理
    ids = request.form.get('ids')
    print ids.split(',')
    print "user: %s delete article id: %s"%(username, ids)
    return redirect(url_for('resource.article', username=current_user.name))

@main.route('/<string:username>/category')
@login_required
def category(username):
    # 文章目录管理
    return render_template('resources/blog/category.html')

@main.route('/<string:username>/keyword')
@login_required
def keyword(username):
    # 关键词管理
    return render_template('resources/blog/keyword.html')