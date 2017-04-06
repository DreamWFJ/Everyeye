# -*- coding: utf-8 -*-
# ===================================
# ScriptName : views.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-04-05 10:47
# ===================================


from app import sql_db as db
from flask import render_template, flash,  redirect, url_for, abort
from .. import resource_blueprint as person
from app.core.db.sql.models import User, Role
from app.utils.decorators import permission_required
from flask_login import login_required, current_user
from .forms import EditProfileForm, EditProfileAdminForm


@person.route('/user/<name>')
@login_required
def user(name):
    user = User.query.filter_by(name=name).first()
    if user is None:
        abort(404)
    return render_template('resources/user/user.html', user=user)


@person.route('/edit-profile', methods = ['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.update_address(form.address_name.data, form.address_country.data, form.address_city.data,
                            form.address_detail.data)
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', name = current_user.name))
    form.name.data = current_user.name
    address = current_user.get_default_address()
    if address:
        form.address_name.data = address.address_name
        form.address_country.data = address.address_country
        form.address_city.data = address.address_city
        form.address_detail.data = address.address_detail
    form.about_me.data = current_user.about_me
    return render_template('resources/user/edit_profile.html', form = form)

@person.route('/edit-profile/<int:id>', methods = ['GET', 'POST'])
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
    return render_template('resources/user/edit_profile.html', form = form, user = user)