# -*- coding: utf-8 -*-
# ===================================
# ScriptName : views.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-04-05 10:42
# ===================================

from flask_login import login_required, current_user
from flask import render_template, request, url_for
from .. import resource_blueprint as main
from app.core.db.sql.models import ActionLog, AuditLog

@main.route('/<string:user_id>/action-log')
@login_required
def action_log(user_id):
    page = int(request.args.get('page', 1))
    page_size = request.args.get('page_size', 10)
    order_name = request.args.get('order_name', 'id')
    order_direction = request.args.get('order_direction', 'asc')
    if page_size == 'all':
        offset_size = page_size = None
    else:
        page_size = int(page_size)
        offset_size = (page - 1) * page_size

    filter_result = ActionLog.query.filter_by(user_id=user_id).order_by(eval("ActionLog.%s.%s()"%(order_name, order_direction)))

    page_result = filter_result.limit(page_size).offset(offset_size)

    return render_template('resources/log/action_log.html', action_log_list=page_result,
                           page_size=request.args.get('page_size', 10), page=request.args.get('page', 1),
                           current_url=url_for('resource.action_log', user_id=current_user.id), query_size=filter_result.count())


@main.route('/<string:user_id>/audit-log')
@login_required
def audit_log(user_id):
    page = int(request.args.get('page', 1))
    page_size = request.args.get('page_size', 10)
    order_name = request.args.get('order_name', 'id')
    order_direction = request.args.get('order_direction', 'asc')
    if page_size == 'all':
        offset_size = page_size = None
    else:
        page_size = int(page_size)
        offset_size = (page - 1) * page_size

    filter_result = AuditLog.query.filter_by(user_id=user_id).order_by(eval("AuditLog.%s.%s()"%(order_name, order_direction)))

    page_result = filter_result.limit(page_size).offset(offset_size)

    return render_template('resources/log/audit_log.html', audit_log_list=page_result,
                           page_size=request.args.get('page_size', 10), page=request.args.get('page', 1),
                           current_url=url_for('resource.audit_log', user_id=current_user.id), query_size=filter_result.count())
