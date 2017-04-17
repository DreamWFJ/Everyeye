#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       views.py
CreateTime:     2017-04-15 16:17
"""

from flask_login import login_required
from flask import render_template, abort
from .. import resource_blueprint as main
from app.core.db.sql.models import User, Log
from app.utils.decorators import permission_required

@main.route('/article/<uuid:article_id>')
@login_required
def someone_article(article_id):
    print "request article id: <%s>"%id
    return render_template('resources/blog/post.html')


@main.route('/article')
@login_required
def article():
    return render_template('resources/blog/index.html')

@main.route('/write_article')
@login_required
def write_article():
    return render_template('resources/blog/write_article.html')

@main.route('/category')
@login_required
def category():
    return render_template('resources/blog/category.html')