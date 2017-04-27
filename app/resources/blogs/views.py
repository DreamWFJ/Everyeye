#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       views.py
CreateTime:     2017-04-15 16:17
"""

from flask_login import login_required
from flask import render_template, request
from .. import resource_blueprint as main
from ..common import get_user_article_categorys, get_user_article_keywords, get_user_article_sources


@main.route('/<string:username>/article/<uuid:article_id>')
@login_required
def one_article(username, article_id):
    print "request article id: <%s>"%id
    return render_template('resources/blog/one_article.html')

@main.route('/<string:username>')
@login_required
def user_index(username):
    print "show_user: ", username
    return render_template('resources/blog/index.html')

@main.route('/<string:username>/article')
@login_required
def article(username):
    return render_template('resources/blog/article.html')

@main.route('/manage_article')
@login_required
def manage_article():
    return render_template('resources/blog/manage_article.html')


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
        if len(content) == 0:
            content = request.form.get('markdown_content')
        reference_links = request.form.getlist('reference_links_box[]')
        return render_template('resources/blog/new_article.html')

@main.route('/<string:username>/category')
@login_required
def category(username):
    # 文章目录
    return render_template('resources/blog/category.html')

@main.route('/<string:username>/keyword')
@login_required
def keyword(username):
    return render_template('resources/blog/keyword.html')