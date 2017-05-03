#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       views.py
CreateTime:     2017-04-15 16:17
"""
import os
import re
from uuid import uuid4
import markdown
import random
from config import upload_image_path
from app.core.db.sql.models import Article, ArticleReferenceLink, ArticleCategory, ArticleComment, ArticleKeyword, User
from flask_login import login_required, current_user
from flask import render_template, request, redirect, url_for, send_from_directory, current_app
from .. import resource_blueprint as main
from app import sql_db
from ..common import get_user_article_categorys, get_user_article_keywords, get_user_article_sources

class UploadImageNameError(Exception):
    pass

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

    page = int(request.args.get('page', 1))
    page_size = request.args.get('page_size', 10)
    order_name = request.args.get('order_name', 'id')
    order_direction = request.args.get('order_direction', 'asc')
    if page_size == 'all':
        offset_size = page_size = None
    else:
        page_size = int(page_size)
        offset_size = (page - 1) * page_size

    # article_list = Article.query.order_by(Article.id).all()
    result_sql = "select articles.*, (select count(*) from article_keyword, article_keywords where " \
                 "article_keyword.id = article_keywords.keyword_id and articles.id = article_keywords.article_id ) as keywords, " \
                 "(select count(*) from article_view_records where article_view_records.article_id = articles.id) as view_count, " \
                 "(select count(*) from article_comments where article_comments.article_id = articles.id) as comment_count from articles"

    page_result = sql_db.session.execute(result_sql)

    return render_template('resources/blog/article.html', article_list=page_result,
                           page_size=request.args.get('page_size', 10), page=request.args.get('page', 1),
                           current_url=url_for('resource.article', username=current_user.name), query_size=10, article_categorys=get_user_article_categorys(),
                           article_keywords=get_user_article_keywords(), article_sources=get_user_article_sources())

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
    return render_template('resources/blog/one_article.html', article=article,
                           current_url=url_for('resource.article', username=current_user.name, article_id=article_id),
                           article_categorys=get_user_article_categorys(), article_keywords=get_user_article_keywords(),
                           article_sources=get_user_article_sources(), article_comments=article_comments,
                           article_comments_total=article_comments_total)

@main.route('/<string:username>/new-article', methods=['POST','GET'])
@login_required
def new_article(username):
    # 写文章
    if request.method == 'GET':
        article_id = request.args.get('article_id')
        if article_id:
            article = Article.query.filter_by(id=article_id).first()
            keywords = ','.join([keyword.name for keyword in article.keywords])
            reference_links_string_list = [reference_link.name for reference_link in article.reference_links.all()]
            setattr(article, 'keywords_string', keywords)
            setattr(article, 'reference_links_string_list', reference_links_string_list)

            print article.category_id
            # print article.reference_links_string
        else:
            article = None
            keywords = None
        print article

        return render_template('resources/blog/new_article.html', article_categorys=get_user_article_categorys(),
                               article_keywords=get_user_article_keywords(), article_sources=get_user_article_sources(),
                               edit_article=article)
    elif request.method == 'POST':
        current_app.logger.debug(request.form)
        title = request.form.get('title')
        category_id = request.form.get('category_id')
        source_id = request.form.get('source_id')
        keywords = request.form.get('keywords')
        status = bool(request.form.get('status'))
        permit_comment = bool(request.form.get('permit_comment'))
        content = request.form.get('summernote_content')
        content_type = "summernote"
        if len(content) == 0:
            content = request.form.get('markdown_content')
            content_type = "markdown"
        reference_links = request.form.getlist('reference_links_box[]')

        article_id = request.args.get('article_id')
        # 允许上传的图片
        def allowed_file(filename):
            return '.' in filename and \
                   filename.rsplit('.', 1)[1] in set(['png', 'jpg', 'jpeg', 'gif'])
        # 转换图片名为uuid
        def secure_filename(filename):
            image_format = filename.rsplit('.', 1)[1]
            return "%s.%s"%(str(uuid4()), image_format)
        file = request.files.get('image')
        image_name = None
        # 图片保存
        if file and allowed_file(file.filename):
            image_name = secure_filename(file.filename)
            user_upload_image_path = os.path.join(upload_image_path, username)
            if not os.path.isdir(user_upload_image_path):
                os.makedirs(user_upload_image_path)
            file.save(os.path.join(user_upload_image_path, image_name).replace('\\', '/'))

        keyword_color_dict = {
            "1":"default",
            "2":"primary",
            "3":"success",
            "4":"info",
            "5":"warning",
            "6":"danger"
        }
        keyword_list = keywords.split(',')
        article_keywords = []
        for keyword in keyword_list:
            article_keyword = ArticleKeyword.insert_keyword(keyword, random.choice(keyword_color_dict.values()))
            article_keywords.append(article_keyword)
        if article_id:
            Article.update_article(article_id, title, article_keywords, source_id, category_id, status, permit_comment, image_name, content, content_type, reference_links)
        else:
            Article.insert_article(current_user.id, title, article_keywords, source_id, category_id, status, permit_comment, image_name, content, content_type, reference_links)
        return redirect(url_for('resource.article', username=current_user.name))




@main.route('/<string:username>/upload/<string:filename>', methods=['POST','GET'])
def uploaded_file(username, filename):
    return send_from_directory(os.path.join(upload_image_path, username).replace('\\', '/'),filename)

@main.route('/<string:username>/delete-article', methods=['POST'])
@login_required
def delete_article(username):
    # 文章目录管理
    ids = request.form.get('ids')
    Article.delete_article_by_ids(ids.split(','))
    print "user: %s delete article id: %s"%(username, ids)
    return "Delete ids '%s' success"%ids

@main.route('/<string:username>/category', methods=['POST','GET'])
@login_required
def category(username):
    # 文章目录管理
    if request.method == "POST":
        name = request.form.get("name")
        status = request.form.get("status")
        status = True if status == "on" else False
        ArticleCategory.insert_category(name, status)
    page = int(request.args.get('page', 1))
    page_size = request.args.get('page_size', 10)
    order_name = request.args.get('order_name', 'id')
    order_direction = request.args.get('order_direction', 'asc')
    if page_size == 'all':
        offset_size = page_size = None
    else:
        page_size = int(page_size)
        offset_size = (page - 1) * page_size

    result_sql = "select article_categorys.*, (select count(*) from articles where articles.category_id = " \
                 "article_categorys.id) as article_count from article_categorys"

    page_result = sql_db.session.execute(result_sql)

    return render_template('resources/blog/category.html', category_list=page_result,
                           page_size=request.args.get('page_size', 10), page=request.args.get('page', 1),
                           current_url=url_for('resource.category', username=current_user.name), query_size=10)

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

@main.route('/<string:user_id>/comment/<string:article_id>', methods=['POST'])
@login_required
def comment(user_id, article_id):
    # 文章评论管理
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