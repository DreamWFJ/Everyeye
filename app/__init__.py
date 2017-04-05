# -*- coding: utf-8 -*-
# ===================================
# ScriptName : __init__.py.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-27 15:43
# ===================================

from flask import Flask, render_template
from flask_mail import Mail
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from config import load_config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
sql_db = SQLAlchemy()
pagedown = PageDown()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(load_config(config_name))
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    sql_db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    from .core.resources import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .core.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix = '/auth')

    from .core.resources import manage as manage_blueprint
    app.register_blueprint(manage_blueprint, url_prefix = '/manage')
    #
    # from .api_1_0 import api as api_1_0_blueprint
    # app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')


    return app

class MySQLAlchemy(SQLAlchemy):
    def init_database(self, **kwargs):
        database = kwargs.pop('database', None)

        self.session.add()
