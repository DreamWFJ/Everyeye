# -*- coding: utf-8 -*-
# ===================================
# ScriptName : __init__.py.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-27 15:43
# ===================================

from flask import Flask
from flask_mail import Mail
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from config import load_config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
sql_db = SQLAlchemy()
pagedown = PageDown()
login_manager = LoginManager()
socketio = SocketIO(async_mode=None)
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
    socketio.init_app(app)

    from .resources import resource_blueprint
    # app.register_blueprint(resource_blueprint, static_folder='static', template_folder='templates')
    app.register_blueprint(resource_blueprint)

    from .core.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix = '/auth')

    from .core.manage import manage_blueprint
    app.register_blueprint(manage_blueprint, url_prefix = '/manage')

    from .api import api_v1_blueprint
    app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1.0')


    return app
