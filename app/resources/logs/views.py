# -*- coding: utf-8 -*-
# ===================================
# ScriptName : views.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-04-05 10:42
# ===================================

from flask_login import login_required, current_user
from flask import render_template, request, url_for, send_file, abort
from .. import resource_blueprint as main
from app.core.db.sql.models import ActionLog, AuditLog
from app.core.common.download import write_xls, write_json, write_csv, write_txt

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

@main.route('/<string:user_id>/action-log/download')
@login_required
def download_action_log(user_id):
    file_type = request.args.get('type')
    headings = ['ID', 'Action', 'Resource', 'Result', 'Detail', 'Time']
    action_logs = ActionLog.query.filter_by(user_id=user_id).all()
    data = [(one.id, one.action, one.resource, one.status, one.detail, one.create_at.strftime('%c')) for one in action_logs]
    if file_type == "excel":
        filename = write_xls(current_user.name, 'action_log', 'sheet 1', headings, data)
    elif file_type == 'json':
        data_list_dict = [dict(one) for one in map(lambda values:zip(headings, values), data)]
        filename = write_json(current_user.name, 'action_log', data_list_dict)
    elif file_type == 'csv':
        filename = write_csv(current_user.name, 'action_log', headings, data)
    elif file_type == 'txt':
        filename = write_txt(current_user.name, 'action_log', headings, data)
    else:
        abort(404)
    return send_file(filename, as_attachment=True, conditional=True)

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

@main.route('/<string:user_id>/audit-log/download')
@login_required
def download_audit_log():
    file_name = request.args.get('filename').strip('.xls')
    # write_xls('audit_log', 'sheet 1', headings, data)