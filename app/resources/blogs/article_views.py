#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       article_views.py
CreateTime:     2017-05-03 19:41
"""

import os
import markdown
from config import upload_image_path
from app.core.db.sql.models import Article, ArticleComment
from flask_login import login_required, current_user
from flask import render_template, request,url_for, send_from_directory, current_app
from .. import resource_blueprint as main
from ..common import get_user_article_categorys, get_user_article_keywords, get_user_article_sources
from .handle import get_keywords_cloud


# @main.route('/<string:username>/article/<uuid:article_id>')
@main.route('/<string:username>/article/<int:article_id>')
@login_required
def one_article(username, article_id):
    # 某一篇文章
    article = Article.query.filter_by(id=article_id).first()
    if article.content_type == "markdown":
        article.content = markdown.markdown(article.content)
    article_comments_total = ArticleComment.query.filter_by(article_id=article_id).count()
    article_comments = ArticleComment.get_article_comments(article_id)
    # 获取侧边关键词云数据
    keywords_cloud = get_keywords_cloud(username)
    return render_template('resources/blog/one_article.html', article=article,
                           current_url=url_for('resource.article', username=current_user.name, article_id=article_id),
                           article_categorys=get_user_article_categorys(), article_keywords=get_user_article_keywords(),
                           article_sources=get_user_article_sources(), article_comments=article_comments,
                           article_comments_total=article_comments_total, keywords_cloud=keywords_cloud)

@main.route('/<string:username>/upload/<string:filename>', methods=['POST','GET'])
def uploaded_file(username, filename):
    return send_from_directory(os.path.join(upload_image_path, username).replace('\\', '/'),filename)