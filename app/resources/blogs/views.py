#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       views.py
CreateTime:     2017-04-15 16:17
"""
import os
from uuid import uuid4
from sqlalchemy import and_, or_
import random
from config import upload_image_path
from app.core.db.sql.models import Article, article_keywords, ArticleKeyword
from flask_login import login_required, current_user
from flask import render_template, request, redirect, url_for, send_from_directory, current_app
from .. import resource_blueprint as main
from app import sql_db
from ..common import get_user_article_categorys, get_user_article_keywords, get_user_article_sources

@main.route('/<string:username>')
@login_required
def user_index(username):
    # 用户主页，这里展示文章简介
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
    source_id = request.args.get('source_id')
    category_id = request.args.get('category_id')
    keyword_id = request.args.get('keyword_id')
    # article_list = Article.query.order_by(Article.id).all()

    if source_id or category_id or keyword_id:
        filter_result = Article.query.filter(or_(Article.source_id==source_id, Article.category_id==category_id, Article.keywords.query.filter_by(id=keyword_id).first()))
    else:
        filter_result = Article.query
    order_result = filter_result.order_by(eval("Article.%s.%s()"%(order_name, order_direction)))
    page_result = order_result.limit(page_size).offset(offset_size)

    # result_sql = "select articles.*, (select count(*) from article_keyword, article_keywords where " \
    #              "article_keyword.id = article_keywords.keyword_id and articles.id = article_keywords.article_id ) as keywords, " \
    #              "(select count(*) from article_view_records where article_view_records.article_id = articles.id) as view_count, " \
    #              "(select count(*) from article_comments where article_comments.article_id = articles.id) as comment_count from articles"
    #
    # page_result = sql_db.session.execute(result_sql)

    return render_template('resources/blog/article.html', article_list=page_result,
                           page_size=request.args.get('page_size', 10), page=request.args.get('page', 1),
                           current_url=url_for('resource.article', username=current_user.name), query_size=order_result.count(),
                           article_categorys=get_user_article_categorys(),
                           article_keywords=get_user_article_keywords(), article_sources=get_user_article_sources())



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
                               article=article)
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


@main.route('/<string:username>/delete-article', methods=['POST'])
@login_required
def delete_article(username):
    # 文章目录管理
    ids = request.form.get('ids')
    Article.delete_article_by_ids(ids.split(','))
    print "user: %s delete article id: %s"%(username, ids)
    return "Delete ids '%s' success"%ids