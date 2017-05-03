#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       comment_views.py
CreateTime:     2017-05-03 19:41
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


@main.route('/<string:user_id>/comment/<string:article_id>', methods=['POST'])
@login_required
def comment(user_id, article_id):
    # 文章评论管理
    if request.method == "POST":
        print request.form
        current_app.logger.debug("user_id: %s, article_id: %s"%(user_id, article_id))
        current_app.logger.debug(request.form)
        reply_to_comment_id = request.form.get('reply_to_comment_id')
        content = request.form.get('content')
        if reply_to_comment_id:
            ArticleComment.add_reply(user_id, reply_to_comment_id, article_id, content)
        else:
            ArticleComment.add_comment(user_id, article_id, content)
        username = User.query.filter_by(id=user_id).first().name
        return redirect(url_for('resource.one_article', username=username, article_id=article_id))


@main.route('/<string:username>/delete-comment', methods=['POST'])
@login_required
def delete_comment(username):
    # 文章目录管理
    ids = request.form.get('ids')
    print ids.split(',')
    # ArticleKeyword.delete_keyword_by_ids(ids.split(','))
    print "user: %s delete comment id: %s"%(username, ids)
    return "Delete ids '%s' success"%ids