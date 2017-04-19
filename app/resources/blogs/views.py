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


@main.route('/article/<uuid:article_id>')
@login_required
def someone_article(article_id):
    print "request article id: <%s>"%id
    return render_template('resources/blog/post.html')

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

@main.route('/<string:username>/write_article', methods=['POST','GET'])
@login_required
def write_article(username):
    if request.method == 'GET':
        return render_template('resources/blog/write_article.html')
    elif request.method == 'POST':
        print request.form
        return render_template('resources/blog/write_article.html')

@main.route('/<string:username>/category')
@login_required
def category(username):
    return render_template('resources/blog/category.html')

@main.route('/<string:username>/keyword')
@login_required
def keyword(username):
    return render_template('resources/blog/keyword.html')