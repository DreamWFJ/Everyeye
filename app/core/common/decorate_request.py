# -*- coding: utf-8 -*-
# ===================================
# ScriptName : decorate_request.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-04-27 9:21
# ===================================


# @app.before_request
# def csrf_protect():
#     if request.method == "POST":
#         token = session.pop('_csrf_token', None)
#         if not token or token != request.form.get('_csrf_token'):
#             abort(403)
#
# def generate_csrf_token():
#     if '_csrf_token' not in session:
#         session['_csrf_token'] = some_random_string()
#     return session['_csrf_token']

# app.jinja_env.globals['csrf_token'] = generate_csrf_token
# Form 中使用csrf
# <input name=_csrf_token type=hidden value="{{ csrf_token() }}">

#         // XSRF 使用
# //        var csrftoken = $('meta[name=csrf-token]').attr('content');
# //        $.ajaxSetup({
# //            beforeSend: function(xhr, settings) {
# //                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
# //                    xhr.setRequestHeader("X-CSRFToken", csrftoken)
# //                }
# //            }
# //        });
#         // Form中使用
# //        {{ form.csrf_token }}