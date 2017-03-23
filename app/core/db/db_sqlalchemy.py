#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author:         WFJ
Version:        0.1.0
FileName:       db_sqlalchemy.py
CreateTime:     2017-03-22 21:52
"""

# -*- coding: utf-8 -*-
# ===================================
# ScriptName : sqlalchemy.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-08 19:56
# ===================================
from .base import UserDatastore, SQLAlchemyDatastore, Datastore
from flask import current_app
from werkzeug.local import LocalProxy
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, PickleType, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session

Base = declarative_base()


class SqlalchemyBackend(Datastore):
    def __init__(self, app):
        self.engine = create_engine(app.config["DATABASE_URL"], convert_unicode=True)
        self.session = scoped_session(sessionmaker(autocommit=False,
                                                      autoflush=False,
                                                      bind=self.engine))
        setattr(self.engine, 'session', self.session)
        super(SqlalchemyBackend, self).__init__(self.db)

        self.user = SQLAlchemyUserDatastore(self.engine, User, Role)

class SQLAlchemyBackend(object):
    def __init__(self, app):
        self.engine = create_engine(app.config["DATABASE_URL"], convert_unicode=True)
        self.session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=self.engine))
        setattr(self.engine, 'session', self.session)

    def add_user(self, email, password, telephone=None, active=True, extra={}, description=''):
        _id = 1
        self.session.add(User(_id=_id, email=email, telephone=telephone, password=password, active=active, extra=extra, description=description))
        self.session.commit()
        return _id

    def query_user(self, name):
        return self.session.query(User).filter(User.name.in_([name])).order_by(User._id).all()
        # query.filter(User.name.like('%name%')) 模糊查询， ilike 大小写敏感， in_, is_(None), isnot(None), or_, and_, match,

    def get_all_user(self):
        return self.session.query(User.name, User._id).all()

class User(Base):
    __tablename__ = 'users'
    _id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=True)
    telephone = Column(String, unique=True)
    password = Column(String, nullable=True)
    active = Column(Boolean)
    create_at = Column(DateTime)
    last_active_at = Column(DateTime)
    extra = Column(PickleType)
    description = Column(String)
    role_id = Column(Integer, ForeignKey('role.id'))
    role = relationship("Role", back_populates="user")

    def __repr__(self):
        return "<User (Email='%s', Telephone='%s', Password='%s')>" % (self.email, self.telephone, self.password)

class Role(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    create_at = Column(DateTime)
    extra = Column(PickleType)
    description = Column(String)
    user = relationship("User", order_by=User.id, back_populates="role")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Role: (name='%r')>" % self.name



class SQLAlchemyUserDatastore(SQLAlchemyDatastore, UserDatastore):
    """A SQLAlchemy datastore implementation for Flask-Security that assumes the
    use of the Flask-SQLAlchemy extension.
    """
    def __init__(self, db, user_model, role_model):
        SQLAlchemyDatastore.__init__(self, db)
        UserDatastore.__init__(self, user_model, role_model)

    def init_database_data(self):
        print "init_database_data"

    def create_one(self):
        print "create_one: ", self.user_model.__name__

    def drop_one(self):
        print "drop_one: ", self.user_model.__name__

    def get_user(self, identifier):
        if self._is_numeric(identifier):
            return self.user_model.query.get(identifier)
        query = getattr(self.user_model, 'email').ilike(identifier)
        rv = self.user_model.query.filter(query).first()
        if rv is not None:
            return rv

    def _is_numeric(self, value):
        try:
            int(value)
        except (TypeError, ValueError):
            return False
        return True

    def find_user(self, **kwargs):
        return self.user_model.query.filter_by(**kwargs).first()

    def find_role(self, role):
        return self.role_model.query.filter_by(name=role).first()

