# -*- coding: utf-8 -*-
# ===================================
# ScriptName : handle.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-05-04 17:16
# ===================================

from sqlalchemy import and_
from app.core.db.sql.models import Article, ArticleComment, ArticleKeywords, User, Keyword, ArticleCategory


def get_keywords_cloud(username):
    # 注意，这里需要按照关键词的文章数来倒排，只获取前10左右的关键词
    user = User.query.filter_by(name=username).first()
    article_list = Article.query.filter_by(user=user).all()
    keywords_set = set()
    for article in article_list:
        keywords = Keyword.query.filter(Keyword.articles.any(ArticleKeywords.article==article)).all()
        for keyword in keywords:
            keywords_set.add(keyword)
    return list(keywords_set)


def get_category_side_nav(username):
    # 这里也需要获取所有的目录，按文章数排序
    user = User.query.filter_by(name=username).first()
    article_list = Article.query.filter_by(user=user).all()
    categorys_set = set()
    for article in article_list:
        categorys = ArticleCategory.query.filter(ArticleCategory.articles.contains(article)).all()
        [categorys_set.add(category) for category in categorys]
    return list(categorys_set)


def get_similar_article(username, article_id):
    user = User.query.filter_by(name=username).first()
    article = Article.query.filter_by(id=article_id).first()
    articles_set = set()
    for keyword in article.keywords:
        print keyword.keyword.name
        similar_articles = Article.query.filter(and_(Article.user_id==user.id, Article.id!=article_id, ArticleKeywords.keyword==keyword)).all()
        if len(similar_articles) == 0:
            continue
        [articles_set.add(article) for article in similar_articles]
    return list(articles_set)