# -*- coding: utf-8 -*-
# ===================================
# ScriptName : sqlalchemy.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-08 19:56
# ===================================
from .base import BaseDatabase
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class SQLAlchemyDB(BaseDatabase):
    def __init__(self):
        pass

    def create_tables(self):
        pass

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    telephone = db.Column(db.Integer, unique=True)
    enabled = db.Column(db.Boolean)
    create_at = db.Column(db.DateTime)
    last_active_at = db.Column(db.DateTime)
    extra = db.Column(db.String)
    description = db.Column(db.String(120), unique=True)

    def __init__(self, user_name):
        self.user_name = user_name

    def __repr__(self):
        return '<User %r>' % self.user_name

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(80), unique=True)
    enabled = db.Column(db.Boolean)
    create_at = db.Column(db.DateTime)
    last_active_at = db.Column(db.DateTime)
    extra = db.Column(db.String)
    description = db.Column(db.String(120), unique=True)

    def __init__(self, role_name):
        self.role_name = role_name

    def __repr__(self):
        return '<Role %r>' % self.role_name


class Right(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    right_name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(120), unique=True)
    enabled = db.Column(db.Boolean)
    create_at = db.Column(db.DateTime)
    last_active_at = db.Column(db.DateTime)
    extra = db.Column(db.String)

    def __init__(self, right_name):
        self.right_name = right_name

    def __repr__(self):
        return '<Right %r>' % self.right_name

class UserGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_group_name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(120), unique=True)
    enabled = db.Column(db.Boolean)
    create_at = db.Column(db.DateTime)
    last_active_at = db.Column(db.DateTime)
    extra = db.Column(db.String)

    def __init__(self, user_group_name):
        self.user_group_name = user_group_name

    def __repr__(self):
        return '<UserGroup %r>' % self.user_group_name

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resource_name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(120), unique=True)
    enabled = db.Column(db.Boolean)
    create_at = db.Column(db.DateTime)
    last_active_at = db.Column(db.DateTime)
    extra = db.Column(db.String)

    def __init__(self, resource_name):
        self.resource_name = resource_name

    def __repr__(self):
        return '<Resource %r>' % self.resource_name

class Passward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(256))
    user_id = db.Column(db.Integer, unique=True)
    create_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)
    extra = db.Column(db.String)

    def __init__(self, user_id, password):
        self.user_id = user_id
        self.password = password

    def __repr__(self):
        return '<Passward for user_id: %r>' % self.user_id

class IDMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True)
    role_id = db.Column(db.Integer, unique=True)
    right_id = db.Column(db.Integer, unique=True)
    resource_id = db.Column(db.Integer, unique=True)
    enabled = db.Column(db.Boolean)
    create_at = db.Column(db.DateTime)
    last_active_at = db.Column(db.DateTime)
    extra = db.Column(db.String)

    def __init__(self, user_id, role_id, right_id, resource_id):
        self.user_id = user_id
        self.role_id = role_id
        self.right_id = right_id
        self.resource_id = resource_id

    def __repr__(self):
        return '<IDMap user_id:%r, role_id:%r, right_id:%r, resource_id:%r>' % (self.user_id, self.role_id, self.right_id, self.resource_id)