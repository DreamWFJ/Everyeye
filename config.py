# -*- coding: utf-8 -*-
# ===================================
# ScriptName : config.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-07 15:00
# ===================================

import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    DB_BACKEND = "sqlalchemy"
    DATABASE = os.path.join(BASE_DIR, 'test.db')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = os.environ.get('MAIL_SENDER')
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    FLASKY_POSTS_PER_PAGE = 20
    FLASKY_FOLLOWERS_PER_PAGE = 50
    FLASKY_COMMENTS_PER_PAGE = 50
    SQLACHEMY_RECORD_QUERIES = True
    FLASKY_SLOW_DB_QUERY_TIME = 0.5
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'data.sqlite').replace('\\', '/')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    URL_PREFIX = 'api'
    API_VERSION = '1.0'
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL')

class TestingConfig(Config):
    DB_BACKEND = "sqlalchemy"
    TESTING = True
    # mysql://username:password@server/db
    SQLALCHEMY_DATABASE_URI = 'sqlite://' + BASE_DIR + '//test.db'
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    DB_BACKEND = "pymongo"
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

config = {
    'development': DevelopmentConfig,
    'test': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
    