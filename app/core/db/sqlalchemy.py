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
db = LocalProxy(lambda: current_app.extensions['every_eye_api'].db_handler)
print db

# roles = db.Table('roles',
#     db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
# )

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    telephone = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(256), )
    active = db.Column(db.Boolean)
    create_at = db.Column(db.DateTime)
    last_active_at = db.Column(db.DateTime)
    extra = db.Column(db.PickleType)
    description = db.Column(db.String(256))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User Email Account: %r>' % self.email

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    create_at = db.Column(db.DateTime)
    extra = db.Column(db.PickleType)
    description = db.Column(db.String(256))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role: %r>' % self.name


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

class SQLAlchemyCommand(Datastore):
    def __init__(self):
        self.user = SQLAlchemyUserDatastore(db,
                                            User(1, 'admin@test.com', '18612082212', 'abc123', True, '2017-03-20 16:00:00', '2017-03-20 16:00:00', {}, '', 1),
                                            Role(1, 'admin', '2017-03-20 16:00:00', {}, ''))
        super(SQLAlchemyCommand, self).__init__(db)

    def create_one(self, database):
        if database == "user":
            self.user.create_one()

    def drop_one(self, database):
        pass

    def create_all(self):
        self.user.create_one()

    def drop_all(self):
        pass
