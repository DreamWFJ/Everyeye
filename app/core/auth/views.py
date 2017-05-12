# -*- coding: utf-8 -*-
# ===================================
# ScriptName : views.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-28 9:31
# ===================================

"""
针对用户后端操作，是想做一个统一的接口，前边web或者api直接调用，避免重复造轮 ------------ 注意------------

"""
from app.utils.email import send_email
from app.core.db.sql.models import User
from .forms import LoginForm, RegistrationForm, ChangeEmailForm, ChangePasswordForm, \
    PasswordResetForm, PasswordResetRequestForm
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from handle import cache_user_right

@auth.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@auth.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """登录用户"""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            current_user.new_audit_log(request.remote_addr)
            return redirect(request.args.get('next') or url_for('resource.user_index', username=current_user.name))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """登出用户"""
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('resource.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """注册一个新的用户"""
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.insert_users(form.username.data,
                          form.email.data,
                          form.password.data)
        # 这个地方应该发送邮件通知用户，注意邮件中附带token，便于用户确认邮箱 -------------- 注意--------------
        token = user.generate_confirmation_token()

        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('resource.index'))
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    """用于账户邮件确认"""
    # 首先检查是否已经确认过
    if current_user.confirmed:
        return redirect(url_for('resource.index'))
    if current_user.confirm_token(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('resource.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    """重新发送确认邮件"""
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('resource.index'))

# before_request 与 before_app_request 请求之前需要处理的事情钩子，一个用于蓝本，一个用于全局
@auth.before_app_request
def before_request():
    """
    同时满足以下 3 个条件时， before_app_request 处理程序会拦截请求。
    (1) 用户已登录（ current_user.is_authenticated() 必须返回 True）。
    (2) 用户的账户还未确认。
    (3) 请求的端点（ 使用 request.endpoint 获取）不在认证蓝本中。访问认证路由要获取权
    限，因为这些路由的作用是让用户确认账户或执行其他账户管理操作
    """
    if current_user.is_authenticated:
        current_user.refresh_last_request_time()
        # 加载用户权限

        cache_user_right(current_user.role_id)
        if not current_user.confirmed and request.endpoint[:5] != 'auth.' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))



@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('resource.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.change_password(form.password.data)
            flash('Your password has been updated')
            return redirect(url_for('resource.index'))
        else:
            flash('Invalid password.')
    return render_template('auth/change_password.html', form = form)

@auth.route('/reset', methods = ['GET', 'POST'])
def password_reset_request():
    """密码重置请求"""
    if not current_user.is_anonymous:
        return redirect(url_for('resource.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            token = user.generate_reset_password_token()
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user = user, token = token,
                       next = request.args.get('next'))
        flash('The reset password link has been sent to your mailbox.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form = form)

@auth.route('/reset/<token>', methods = ['GET', 'POST'])
def password_reset(token):
    if current_user.is_anonymous:
        return redirect(url_for('resource.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user is None:
            return redirect(url_for('resource.index'))
        if user.reset_password(token, form.password.data):
            flash('Your password has been updated')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('resource.index'))
    return render_template('auth/reset_password.html', form = form)

@auth.route('/change-email', methods = ['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       'auth/email/change_email',
                       user = current_user, token = token)
            flash('The confirm email link has been sent to your mailbox.')
            return redirect(url_for('resource.index'))
        else:
            flash('Invalid email or password.')
    return render_template('auth/change_email.html', form = form)

@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('Your email address has been updated')
    else:
        flash('Invalid request')
    return redirect(url_for('resource.index'))