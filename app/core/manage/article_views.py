# -*- coding: utf-8 -*-
# ===================================
# ScriptName : article_views.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-04-20 20:31
# ===================================


from app.core.db.sql.models import User
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import manage_blueprint as manage


@manage.route('/article')
def article():
    return render_template('manage/article/article.html')

@manage.route('/category')
def category():
    return render_template('manage/article/category.html')

@manage.route('/comment')
def comment():
    return render_template('manage/article/comment.html')

@manage.route('/keyword')
def keyword():
    return render_template('manage/article/keyword.html')

@manage.route('/sensitive-word')
def sensitive_word():
    return render_template('manage/article/sensitive_word.html')
