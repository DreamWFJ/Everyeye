#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       common.py
CreateTime:     2017-04-27 21:27
"""
def get_user_article_sources():
    return [
        {
            "id":1, "name":"original"
        },
        {
            "id":2, "name":"quote"
        },
        {
            "id":3, "name":"other"
        }
    ]

def get_user_article_categorys():
    return [
        {
            "id":1, "name":"life"
        },
        {
            "id":2, "name":"python"
        },
        {
            "id":3, "name":"work"
        }
    ]

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