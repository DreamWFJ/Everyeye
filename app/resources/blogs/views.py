#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       views.py
CreateTime:     2017-04-15 16:17
"""
import markdown
from app.core.db.sql.models import Article, ArticleReferenceLink, ArticleCategory, ArticleComment
from flask_login import login_required, current_user
from flask import render_template, request, redirect, url_for
from .. import resource_blueprint as main
from app import sql_db
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
    result_sql = "select articles.*, (select count(*) from article_view_records where article_view_records.article_id = articles.id) as view_count, " \
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
    print "request article id: <%s>"%id
    article = Article.query.filter_by(id=article_id).first()
    if article.content_type == "markdown":
        article.content = markdown.markdown(article.content)
    reference_links = ArticleReferenceLink.query.filter_by(article_id=article_id).all()
    setattr(article, 'reference_links', reference_links)
    return render_template('resources/blog/one_article.html', article=article,
                           current_url=url_for('resource.article', username=current_user.name, article_id=article_id),
                           article_categorys=get_user_article_categorys(), article_keywords=get_user_article_keywords(),
                           article_sources=get_user_article_sources())

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
        status = bool(request.form.get('status'))
        permit_comment = bool(request.form.get('permit_comment'))
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
        print "status : ",status
        print "permit_comment : ",permit_comment
        print "content : ",content
        print "content_type : ",content_type
        print "reference_links : ",reference_links
        print "current_user_id : ",current_user.id
        Article.insert_article(current_user.id, title, keywords, source_id, category_id, status, permit_comment, content, content_type, reference_links)
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

@main.route('/<string:username>/keyword')
@login_required
def keyword(username):
    # 关键词管理
    return render_template('resources/blog/keyword.html')