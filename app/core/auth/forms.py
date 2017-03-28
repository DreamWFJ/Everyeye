# -*- coding: utf-8 -*-
# ===================================
# ScriptName : forms.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-28 10:05
# ===================================

from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')