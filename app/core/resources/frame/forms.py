# -*- coding: utf-8 -*-
# ===================================
# ScriptName : forms.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-30 9:11
# ===================================
from flask_wtf import FlaskForm
from flask_wtf.file import  FileField, FileAllowed, FileRequired

class PhotoForm(FlaskForm):
    upload = FileField('image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])

