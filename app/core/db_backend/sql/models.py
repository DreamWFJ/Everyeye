# -*- coding: utf-8 -*-
# ===================================
# ScriptName : models.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-23 16:42
# ===================================
import hashlib
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask import request, url_for
from markdown import markdown
from app.core.db_backend.mixins import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

_db = SQLAlchemy()

db = _db

# 建立资源与角色的多对多关系
resources = db.Table('resources',
                     db.Column('resource_id', db.Integer, db.ForeignKey('resource.id')),
                     db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
                     db.Column('create_at', db.DateTime, default = datetime.utcnow))


# 角色表
class Role(db.Model):
    __tablename__ = 'roles'
    _id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    enabled = db.Column(db.Boolean, default = True, index = True)
    # 与资源的多对多关系
    resource = db.relationship('Resource',
                               secondary=resources,
                               backref = db.backref('roles', lazy='joined'),
                               lazy='dynamic',
                               cascade = 'all, delete-orphan')
    # 与用户的一对多关系
    users = db.relationship('User', backref = 'roles', lazy = 'dynamic')
    create_at = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Role %r>' % self.name

class Right(db.Model):
    __tablename__ = 'rights'
    _id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    value = db.Column(db.Integer, unique = True)
    create_at = db.Column(db.DateTime(), default = datetime.utcnow)
    resource = db.relationship('Resource', backref = 'rights', lazy = 'dynamic')

    @staticmethod
    def insert_rights():
        rights = {
            'None': (0, 0x00),
            'Show': (1, 0x01),
            'Create': (1, 0x02),
            'Update': (1, 0x04),
            'Delete': (1, 0x08)
        }
        for r in rights:
            right = Right.query.filter_by(name = r).first()
            if right is None:
                right = Right(name = r)
            right._id = rights[r][0]
            right.value = rights[r][1]
            db.session.add(right)
        db.session.commit()

    def __repr__(self):
        return '<Right %r>' % self.name



class Resource(db.Model):
    __tablename__ = 'resource'
    _id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    value = db.Column(db.Integer)
    enabled = db.Column(db.Boolean, default=True, index=True)
    description = db.Column(db.Text(), default=True, index=True)
    right_id = db.Column(db.Integer, db.ForeignKey('rights.id'))
    create_at = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Resource %r>' % self.name


# 关注关系表
class Follow(db.Model):
    __tablename__ = 'follows'
    # 关注者的ID
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key = True)
    # 被关注者的ID
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key = True)
    create_at = db.Column(db.DateTime, default = datetime.utcnow)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    # 用户名名称
    name = db.Column(db.String(64), unique = True, index = True)
    # 邮件地址
    email = db.Column(db.String(64), unique = True, index = True, nullable=True)
    password_hash = db.Column(db.String(128), nullable=True)
    # 是否激活用户，默认激活
    enabled = db.Column(db.Boolean, default = False)
    # 角色ID
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # 其他信息
    extra = db.Column(db.PickleType())
    # 用户地址信息
    addresses = db.relationship('Address', backref = 'user', lazy = 'dynamic')
    # 用户联系方式
    contact = db.relationship('Contact', backref='user', lazy='dynamic')
    # 用户创建时间
    create_at = db.Column(db.DateTime(), default = datetime.utcnow)
    # 博文信息
    posts = db.relationship('Post', backref = 'author', lazy = 'dynamic')
    # 评论信息
    comments = db.relationship('Comment', backref = 'author', lazy = 'dynamic')
    # 登陆登出日志信息
    logs = db.relationship('Log', backref = 'author', lazy = 'dynamic')
    # 被关注者
    followed = db.relationship('Follow',
                               foreign_keys = [Follow.follower_id],
                               backref = db.backref('follower', lazy = 'joined'),
                               lazy = 'dynamic',
                               cascade = 'all, delete-orphan')
    # 关注着
    followers = db.relationship('Follow',
                                foreign_keys = [Follow.followed_id],
                                backref = db.backref('followed', lazy = 'joined'),
                                lazy = 'dynamic',
                                cascade = 'all, delete-orphan')


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration = 3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def generate_reset_token(self, expiration = 3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        db.session.commit()
        return True

    def generate_email_change_token(self, new_email, expiration = 3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in = expiration)
        return s.dumps({'id': self.id})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email = new_email).first() is not None:
            return False
        self.email = new_email
        self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        db.session.add(self)
        db.session.commit()
        return True

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def gravatar(self, size = 100, default = 'identicon', rating = 'g'):
        if request.is_secure:
            url = 'https://cn.gravatar.com/avatar'
        else:
            url = 'http://cn.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url = url, hash = hash, size = size, default = default, rating = rating)

    def follow(self, user):
        if not self.is_following(user):
            f = Follow(follower = self, followed = user)
            db.session.add(f)
            db.session.commit()

    def unfollow(self, user):
        f = self.followed.filter_by(followed_id = user.id).first()
        if f:
            db.session.delete(f)
            db.session.commit()

    def is_following(self, user):
        return self.followed.filter_by(followed_id = user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id = user.id).first() is not None

    def is_like_post(self, post):
        return self.likes.filter_by(post_id = post.id).first() is not None

    def to_json(self):
        json_use = {
            'url': url_for('api_get_user', id = self.id, _external = True),
            'username': self.username,
            'member_since': self.member_since,
            'last_seen': self.last_seen,
            'posts': url_for('api.get_user_posts', id = self.id, _external = True),
            'followed_posts': url_for('api.get_user_followed_posts',
                                      id = self.id, _external = True),
            'post_count': self.posts.count()
        }
        return json_use

    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions = 0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default = True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()
        self.follow(self)

    @staticmethod
    def generate_fake(count = 100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        # 用于产生虚假数据
        import forgery_py

        seed()
        for i in range(count):
            u = User(email = forgery_py.internet.email_address(),
                     username = forgery_py.internet.user_name(True),
                     password = forgery_py.lorem_ipsum.word(),
                     confirmed = True,
                     name = forgery_py.name.full_name(),
                     location = forgery_py.address.city(),
                     about_me = forgery_py.lorem_ipsum.sentence(),
                     member_since = forgery_py.date.date(True))
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    @staticmethod
    def add_self_follows():
        for user in User.query.all():
            if not user.is_following(user):
                user.follow(user)
                db.session.add(user)
                db.session.commit()

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

