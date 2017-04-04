# -*- coding: utf-8 -*-
# ===================================
# ScriptName : views.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-30 9:11
# ===================================

import os
from .. import main
from app import sql_db as db
from datetime import datetime
from flask_login import login_required
from flask import render_template, abort, redirect, url_for, current_app, flash
from app.core.db.sql.models import User, Role, Log
from app.utils.decorators import permission_required
from werkzeug.utils import secure_filename
from flask_login import login_user, login_required, logout_user, current_user
from .forms import PhotoForm, EditProfileForm, EditProfileAdminForm

@main.route('/upload', methods=['GET', 'POST'])
def upload():
    form = PhotoForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            current_app.instance_path, 'photos', filename
        ))
        return redirect(url_for('index'))

    return render_template('upload.html', form=form)

@main.route('/')
def index():
    ct = datetime.utcnow()
    print ct
    return render_template('index.html', current_time=ct)

# 在模板中添加权限变量
@main.app_context_processor
def inject_permissions():
    return dict()

@main.route('/user/<name>')
def user(name):
    user = User.query.filter_by(name=name).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)

@main.route('/user')
@login_required
@permission_required('user', 'show')
def show_user():
    return 'has permission to show user'


@main.route('/edit-profile', methods = ['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash(u'你的个人资料已更新')
        return redirect(url_for('.user', name = current_user.name))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form = form)

@main.route('/edit-profile/<int:id>', methods = ['GET', 'POST'])
@login_required
@permission_required('profile', 'update')
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user = user)
    if form.validate_on_submit():
        user.role = Role.query.get(form.role.data)
        user.update_user(form.name.data, form.real_name.data, form.email.data, (Role.query.get(form.role.data)).id,
                         form.enabled.data, form.confirmed.data, form.about_me.data)
        user.update_address(form.address_name.data, form.address_country.data, form.address_city.data,
                            form.address_detail.data)
        flash('Person data has been updated.')
        return redirect(url_for('.user', name = user.name))
    form.email.data = user.email
    form.name.data = user.name
    form.real_name.data = user.real_name
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.enabled.data = user.enabled
    form.name.data = user.name
    address = user.get_default_address()
    form.address_name.data = address.address_name
    form.address_country.data = address.address_country
    form.address_city.data = address.address_city
    form.address_detail.data = address.address_detail
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form = form, user = user)


@main.route('/log/<name>')
@login_required
@permission_required('log', 'show')
def logs(name):
    user = User.query.filter_by(name=name).first()
    if user is None:
        abort(404)
    logs = Log.query.filter_by(user_id=user.id).all()
    if logs is None:
        abort(404)
    return render_template('log.html', logs=logs)


# 下面是用户、角色、权限、资源管理设置
@main.route('/user-list')
def manage_user():
    return render_template('manage/user.html')

@main.route('/role-list')
def manage_role():
    return render_template('manage/role.html')

@main.route('/right-list')
def manage_right():
    return render_template('manage/right.html')

@main.route('/resource-list')
def manage_resource():
    return render_template('manage/resource.html')



