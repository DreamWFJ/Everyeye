#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       user_views.py
CreateTime:     2017-04-04 20:11
"""

from app.core.db.sql.models import User
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import manage_blueprint as manage

@manage.route('/user', methods=['POST','GET'])
def user():
    if request.method == 'POST':
        print request.form
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        repeat_password = request.form.get('repeat_password')
        if User.query.filter_by(name=username).first():
            flash("Error: username repeat")
        elif User.query.filter_by(email=email).first():
            flash("Error: email repeat")
        else:
            if password == repeat_password:
                User.insert_users(username, email, password)
            else:
                flash("Error: differt password")
    page = int(request.args.get('page', 1))
    page_size = request.args.get('page_size', 10)
    order_name = request.args.get('order_name', 'id')
    order_direction = request.args.get('order_direction', 'asc')
    if page_size == 'all':
        offset_size = page_size = None
    else:
        page_size = int(page_size)
        offset_size = (page - 1) * page_size

    filter_result = User.query.order_by(eval("User.%s.%s()"%(order_name, order_direction)))
    page_result = filter_result.limit(page_size).offset(offset_size)
    return render_template('manage/admin/user.html', users=page_result,
                           page_size=request.args.get('page_size', 10), page=request.args.get('page', 1),
                           current_url=url_for('manage.user'),
                           total=User.query.count(), query_size=filter_result.count())

@manage.route('/user/reset-password', methods=['POST'])
def reset_user_password():
    print request.form
    flash("Info: send email of repeat password to '%s'"%request.form.get('email'))
    return redirect(url_for('manage.user'))


@manage.route('/user/edit-info', methods=['POST'])
def edit_user_info():
    print request.form
    flash('Edit "%s" information success'%request.form.get('username'))
    return redirect(url_for('manage.user'))

@manage.route('/user/bind-role', methods=['POST'])
def bind_user_role():
    print request.form
    flash('Bind "%s" role success'%request.form.get('username'))
    return redirect(url_for('manage.user'))

@manage.route('/user/edit-status')
def edit_user_status():
    print request.args
    flash('Edit "%s" status success'%request.form.get('username'))
    return redirect(url_for('manage.user'))


@manage.route('/profile')
def profile():
    return render_template('manage/admin/profile.html')



@manage.route('/user/delete', methods=['POST'])
def delete_user():
    print request.form
    user_ids = request.form.get('user_ids')
    print user_ids.split(',')
    flash('delete user id "%s" success'%request.form.get('user_ids'))
    return redirect(url_for('manage.user'))

@manage.route('/user/send-email', methods=['POST'])
def send_user_email():
    print request.form.get('email_to')
    print request.form.get('email_subject')
    print request.form.get('email_content')
    flash('send email to "%s" success'%request.form.get('email_to'))
    return redirect(url_for('manage.user'))

@manage.route('/user/search', methods=['POST'])
def user_search():
    print request.form.get('content')
    return redirect(url_for('manage.user'))
