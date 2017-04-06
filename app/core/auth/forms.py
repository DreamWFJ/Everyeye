# -*- coding: utf-8 -*-
# ===================================
# ScriptName : forms.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-28 10:05
# ===================================

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..db.sql.models import User

class LoginForm(FlaskForm):
    """登录表单"""
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    """注册表单"""
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                          'Usernames must have only letters,'
                                                          'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('re_password',
                                                                             message='Passwords must match.')])
    re_password = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('Username already in use.')

class ChangePasswordForm(FlaskForm):
    """修改密码表单"""
    old_password = PasswordField('Old Password', validators = [DataRequired()])
    password = PasswordField('New Password', validators = [
        DataRequired(), EqualTo('re_password', message = 'Passwords must match')])
    re_password = PasswordField('Confirm password', validators = [DataRequired()])
    submit = SubmitField('Update Password')

class PasswordResetRequestForm(FlaskForm):
    """密码重置请求表单"""
    email = StringField('Email', validators = [DataRequired(), Length(1, 64),
                                               Email()])
    submit = SubmitField('Reset Password')

class PasswordResetForm(FlaskForm):
    """密码重置表单"""
    email = StringField('Email', validators = [DataRequired(), Length(1, 64),
                                               Email()])
    password = PasswordField('New Password', validators = [
        DataRequired(), EqualTo('re_password', message = 'Passwords must match()')])
    re_password = PasswordField('Confirm password', validators = [DataRequired()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email = field.data).first() is None:
            raise ValidationError('Invalid email address.')

class ChangeEmailForm(FlaskForm):
    """修改邮件地址表单"""
    email = StringField('New Email', validators = [DataRequired(), Length(1, 64),
                                                   Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Update Email')

    def validate_email(self, field):
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Email has been registered.')