#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       common.py
CreateTime:     2017-04-27 21:27
"""
from app.core.db.sql.models import ArticleCategory, ArticleSource

def get_user_article_sources():
    return ArticleSource.query.order_by(ArticleSource.id)

def get_user_article_categorys():
    return ArticleCategory.query.order_by(ArticleCategory.id)

def get_user_article_keywords():
    # 限制返回8个
    return [
        {
            "id":1, "name":"Aritcle", "color":"default"
        },
        {
            "id":2, "name":"nothing", "color":"primary"
        },
        {
            "id":3, "name":"learning", "color":"success"
        },
        {
            "id":4, "name":"CDN", "color":"info"
        },
        {
            "id":5, "name":"K8S", "color":"warning"
        },
        {
            "id":6, "name":"Cloud", "color":"danger"
        },
        {
            "id":7, "name":"mouse", "color":"default"
        },
        {
            "id":8, "name":"apple", "color":"primary"
        }
    ]