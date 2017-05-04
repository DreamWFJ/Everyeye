# -*- coding: utf-8 -*-
# ===================================
# ScriptName : handle.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-05-04 17:16
# ===================================


from app.core.db.sql.models import Article, ArticleComment, ArticleKeywords, User, Keyword


def get_keywords_cloud(username):
    user = User.query.filter_by(name=username).first()
    article_list = Article.query.filter_by(user=user).all()
    keywords_set = set()
    for article in article_list:
        keywords = Keyword.query.filter(Keyword.articles.any(ArticleKeywords.article==article)).all()
        for keyword in keywords:
            keywords_set.add(keyword)
    return list(keywords_set)