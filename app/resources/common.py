#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       common.py
CreateTime:     2017-04-27 21:27
"""
from app.core.db.sql.models import ArticleCategory, ArticleSource, Keyword

def get_user_article_sources():
    return ArticleSource.query.order_by(ArticleSource.id)

def get_user_article_categorys():
    return ArticleCategory.query.order_by(ArticleCategory.id)

def get_user_article_keywords():
    # 限制返回8个,而且是使用最多的8个
    return Keyword.query.order_by(Keyword.id).limit(8)
