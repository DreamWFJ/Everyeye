# -*- coding: utf-8 -*-
# ===================================
# ScriptName : config.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-27 15:51
# ===================================

import os
import logging
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
upload_image_path = os.path.join(BASE_DIR, 'app/static/img/blogs').replace('\\', '/')

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=os.path.join(BASE_DIR, 'debug.log'),
                filemode='w')

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN') or 'admin@no-replay.com'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'data.sqlite').replace('\\', '/')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    URL_PREFIX = 'api'
    API_VERSION = '1.0'

    @staticmethod
    def init_app(app):
        pass

class Default(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    # 添加邮件前缀
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    # 添加邮件发送者
    FLASKY_MAIL_SENDER = os.environ.get('MAIL_USERNAME')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

class Testing(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://test:test@localhost/everyeye'

class Production(Config):
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

def load_config(env='default'):
    config = {
        'default': Default,
        'testing': Testing,
        'production': Production
    }
    return config[env]