#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       right_views.py
CreateTime:     2017-04-04 20:11
"""

from app.core.db.sql.models import Right
from flask import render_template, request, url_for, flash, redirect
from . import manage_blueprint as manage

@manage.route('/right', methods=['POST','GET'])
def right():
    if request.method == 'POST':
        print request.form
        name = request.form.get('name')
        weight = request.form.get('weight')
        status = request.form.get('status')
        status = True if status == "on" else False
        if Right.query.filter_by(name=name).first():
            flash("Error: right name repeat")
        else:
            Right.insert_rights(name, weight, status)
    page = int(request.args.get('page', 1))
    page_size = request.args.get('page_size', 10)
    order_name = request.args.get('order_name', 'id')
    order_direction = request.args.get('order_direction', 'asc')
    if page_size == 'all':
        offset_size = page_size = None
    else:
        page_size = int(page_size)
        offset_size = (page - 1) * page_size

    filter_result = Right.query.order_by(eval("Right.%s.%s()"%(order_name, order_direction)))
    page_result = filter_result.limit(page_size).offset(offset_size)
    return render_template('manage/admin/right.html', rights=page_result,
                           page_size=request.args.get('page_size', 10), page=request.args.get('page', 1),
                           current_url=url_for('manage.right'),
                           total=Right.query.count(), query_size=filter_result.count())

@manage.route('/right/edit-status')
def edit_right_status():
    print request.args
    flash('Edit "%s" status to "%s" success'%(request.args.get('right_id'), request.args.get('status')))
    return redirect(url_for('manage.right'))

@manage.route('/right/search', methods=['POST'])
def right_search():
    print request.form.get('content')
    return redirect(url_for('manage.right'))


@manage.route('/right/delete', methods=['POST'])
def delete_right():
    print request.form
    ids = request.form.get('ids')
    print ids.split(',')
    flash('delete right ids "%s" success'%request.form.get('ids'))
    return redirect(url_for('manage.right'))

@manage.route('/right/bind-resource', methods=['POST'])
def bind_right_resource():
    print request.form
    flash('Bind "%s" right resource "%s" success'%(request.form.get('name'), request.form.get('resource_id')))
    return redirect(url_for('manage.right'))