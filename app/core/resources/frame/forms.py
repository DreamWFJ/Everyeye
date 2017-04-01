# -*- coding: utf-8 -*-
# ===================================
# ScriptName : forms.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-30 9:11
# ===================================
from flask_wtf import FlaskForm
from flask_wtf.file import  FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, BooleanField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from app.core.db.sql.models import Role, User

class PhotoForm(FlaskForm):
    """照片上传"""
    upload = FileField('image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])

class EditProfileForm(FlaskForm):
    """编辑个人配置"""
    name = StringField('Name', validators = [Length(0, 64)])
    Address = StringField('Address', validators = [Length(0, 64)])
    about_me = TextAreaField('About Me')
    submit = SubmitField('Confirm')

class EditProfileAdminForm(FlaskForm):
    """编辑管理员配置"""
    email = StringField('Email', validators = [DataRequired(), Length(1, 64),
                                               Email()])
    name = StringField('User Name', validators = [
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('Email Is Confirmed ?')
    enabled = BooleanField('User is Actived ?')
    role = SelectField('Role', coerce = int)
    real_name = StringField('Real Name', validators = [Length(0, 64)])
    address_name = StringField('Address Name', validators = [Length(0, 64)])
    address_country = StringField('Address Country', validators = [Length(0, 64)])
    address_city = StringField('Address City', validators = [Length(0, 64)])
    address_detail = StringField('Address Detail', validators = [Length(0, 128)])
    about_me = TextAreaField('About Me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                            for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email = field.data).first():
            raise ValidationError('The Email has already been registered.')

    def validate_name(self, field):
        if field.data != self.user.name and \
                User.query.filter_by(name = field.data).first():
            raise ValidationError('The user name has already been registered.')