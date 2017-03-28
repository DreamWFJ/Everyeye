# -*- coding: utf-8 -*-
# ===================================
# ScriptName : models.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-27 15:44
# ===================================
import hashlib
from flask import request, url_for
from datetime import datetime
from app import sql_db as db
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer
from app.core.common.user_mixin import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash



# 建立资源与角色的多对多关系
resources_roles = db.Table('resources_roles',
                     db.Column('resource_id', db.Integer, db.ForeignKey('resources.id')),
                     db.Column('role_id', db.Integer, db.ForeignKey('roles.id')))

# 建立资源与权限的多对多关系
resources_rights = db.Table('resources_rights',
                  db.Column('resource_id', db.Integer, db.ForeignKey('resources.id')),
                  db.Column('right_id', db.Integer, db.ForeignKey('rights.id')))

# 建立

class Resource(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    right_weight = db.Column(db.Integer)
    enabled = db.Column(db.Boolean, default=True, index=True)
    extra = db.Column(db.PickleType)
    description = db.Column(db.Text())
    create_at = db.Column(db.DateTime, default = datetime.utcnow)

    @staticmethod
    def insert_resources(name, right_weight, enabled=True):

        resource = Resource.query.filter_by(name = name).first()
        if resource is None:
            resource = Resource(name = name)
        resource.right_weight = right_weight
        resource.enabled = enabled
        db.session.add(resource)
        db.session.commit()
        return resource

    def __repr__(self):
        return '<Resource %r>' % self.name

# 角色表
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    enabled = db.Column(db.Boolean, default = True, index = True)
    # 与资源的多对多关系
    resources = db.relationship('Resource',
                               secondary = resources_roles,
                               backref = db.backref('roles', lazy='dynamic'))
    # 与用户的一对多关系
    users = db.relationship('User', backref = 'roles', lazy = 'dynamic')
    create_at = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Role %r>' % self.name

    @staticmethod
    def insert_roles(rolename, resources=None, users=None):

        role = Role.query.filter_by(name = rolename).first()
        if role is None:
            role = Role(name = rolename)
        if resources:
            role.resources = resources
        if users:
            role.users = users
        db.session.add(role)
        db.session.commit()
        return role

class Right(db.Model):
    __tablename__ = 'rights'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    weight = db.Column(db.Integer, unique = True)
    create_at = db.Column(db.DateTime(), default = datetime.utcnow)
    # 与资源的多对多关系
    resources = db.relationship('Resource',
                               secondary=resources_rights,
                               backref = db.backref('rights', lazy='dynamic'))

    @staticmethod
    def insert_rights(name, weight, resources):
        right = Right.query.filter_by(name = name).first()
        if right is None:
            right = Right(name = name)
        right.weight = weight
        if resources:
            right.resources = resources
        db.session.add(right)
        db.session.commit()

    def __repr__(self):
        return '<Right %r>' % self.name

class RightWeight(object):
    """当前只有增、删、改、查、这4种基本权限，若有新的权限，可以在权限库中添加"""
    NONE = 0x00
    SHOW = 0x01
    CREATE = 0x02
    UPDATE = 0x04
    DELETE = 0x08
    ALL = NONE | SHOW | CREATE | UPDATE | DELETE


class Address(db.Model):
    """用户地址信息"""
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key = True)
    # 用户名名称
    name = db.Column(db.String(64), unique=True)
    country = db.Column(db.String(64))
    city = db.Column(db.String(64))
    detail_address = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def insert_rights(name, country, city, detail_address):
        address = Address.query.filter_by(name = name).first()
        if address is None:
            address = Address(name = name)
        address.country = country
        address.city = city
        address.detail_address = detail_address
        db.session.add(address)
        db.session.commit()
        return address

    def __repr__(self):
        return '<Resource %r>' % self.name

class AuditLog(db.Model):
    """用户的登录登出审计日志"""
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key = True)
    login_city = db.Column(db.String(16))
    login_address = db.Column(db.Text())
    ip = db.Column(db.String(16))
    login_time = db.Column(db.DateTime(), default = datetime.utcnow)
    logout_time = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def insert_audit_logs(login_city, login_address, ip, login_time, logout_time=None):
        audit_logs = AuditLog()
        audit_logs.login_city = login_city
        audit_logs.login_address = login_address
        audit_logs.ip = ip
        if login_time:
            audit_logs.login_time = login_time
        if logout_time:
            audit_logs.logout_time = logout_time
        db.session.add(audit_logs)
        db.session.commit()
        return audit_logs

    @staticmethod
    def update_logout_time(_id, logout_time):
        audit_log = AuditLog.query.filter_by(id = _id).first()
        if audit_log is None:
            raise RuntimeError("database audit log lose id='%s' record."%_id)
        audit_log.logout_time = logout_time
        db.session.add(audit_log)
        db.session.commit()


    def __repr__(self):
        return '<AuditLog %r>' % self.name

class Log(db.Model):
    """用户的操作日志"""
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key = True)
    action = db.Column(db.String(64))
    log_detail = db.Column(db.Text())
    create_at = db.Column(db.DateTime(), default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def insert_logs(action, log_detail):
        log = Log()
        log.action = action
        log.log_detail = log_detail
        db.session.add(log)
        db.session.commit()
        return log

    def __repr__(self):
        return '<AuditLog %r>' % self.name

class User(UserMixin, db.Model):
    """用户信息"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    # 用户名名称
    name = db.Column(db.String(64), unique = True, index = True)
    # 邮件地址
    email = db.Column(db.String(64), unique = True, index = True, nullable=True)
    password_hash = db.Column(db.String(128), nullable=True)
    # 是否激活用户，默认激活，管理员可以禁止该用户登录，通过设置该选项 --------------- 注意---------------
    enabled = db.Column(db.Boolean, default = True)
    # 邮件是否确认
    confirmed = db.Column(db.Boolean, default=False)
    # 角色ID
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # 个人标识符哈希值
    avatar_hash = db.Column(db.String(32))
    # 其他信息
    extra = db.Column(db.PickleType())
    # 用户创建时间
    create_at = db.Column(db.DateTime(), default = datetime.utcnow)
    # 用户地址信息
    addresses = db.relationship('Address', backref = 'user', lazy = 'dynamic')
    # 操作日志信息
    logs = db.relationship('Log', backref = 'user', lazy = 'dynamic')
    # 登陆登出的审计日志信息
    audit_logs = db.relationship('AuditLog', backref = 'user', lazy = 'dynamic')

    def __repr__(self):
        return '<User %r>' % self.name

    def generate_confirmation_token(self, expiration=3600):
        """产生一个激活token"""
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm_token(self, token):
        """验证令牌，若成功并标记该用户已经确认邮件"""
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        print "user: %s, token: %s" %(self.name, token)

        try:
            data = s.load(token)
        except:
            return False

        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    @staticmethod
    def insert_users(username, email, password, addresses=None, logs=None, audit_logs=None):
        """说明：该方法需要改进的地方是，通过传入用户名，邮箱，密码之后，需要为其关联普通用户角色，
        角色所能够操作的资源是预分配的"""
        user = User()
        user.name = username
        user.email = email
        if addresses:
            user.addresses = addresses
        if logs:
            user.logs = logs
        if audit_logs:
            user.audit_logs = audit_logs
        user.password_hash = generate_password_hash(password)
        db.session.add(user)
        db.session.commit()
        return user

    def generate_reset_password_token(self, expiration = 3600):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        """重置密码"""
        print "------------ token: %s, new password: %s ---" %(token, new_password)
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
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

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def change_password(self, password):
        """修改密码"""
        self.password_hash = generate_password_hash(password)
        db.session.add(self)
        db.session.commit()

    def generate_email_change_token(self, new_email, expiration = 3600):
        """产生修改邮箱地址的token"""
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        """修改邮箱地址"""
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
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

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_right(self, permissions):
        return True
    # 个人头像标识
    def gravatar(self, size = 100, default = 'identicon', rating = 'g'):
        if request.is_secure:
            url = 'https://cn.gravatar.com/avatar'
        else:
            url = 'http://cn.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url = url, hash = hash, size = size, default = default, rating = rating)

class AnonymousUser(AnonymousUserMixin):
    def is_administrator(self):
        return False

    def has_right(self, permissions):
        return False


class InitData(object):
    """初始化数据库"""
    def __init__(self):
        self.resources = self.create_resources()
        self.user = self.create_user()
        self.create_rights()
        self.create_role()

    def create_log(self):
        action = 'update user name'
        log_detail = 'update user<id=1, name="haha"> to user<id=1, name="lala">, result: successful operation'
        return Log.insert_logs(action, log_detail)

    def create_address(self):
        name = 'my home'
        country = 'China'
        city = 'Beijin'
        detail_address= 'Chao yang country, Beijin, China'
        return Address.insert_rights(name, country, city, detail_address)

    def create_audit_log(self):
        login_city = 'Beijin'
        login_address = 'Beijin of China, chao yang country'
        ip = '192.168.1.123'
        login_time = datetime.now()
        logout_time = datetime.now()
        return AuditLog.insert_audit_logs(login_city, login_address, ip, login_time, logout_time)

    def create_user(self):
        username = 'Administrator'
        email = 'admin@no-replay.com'
        password = 'this_is_a_test_acount'
        address = self.create_address()
        print address.detail_address
        log = self.create_log()
        print log.log_detail
        audit_log = self.create_audit_log()
        print audit_log.ip
        return User.insert_users(username, email, password,
                                 addresses=[address], logs=[log], audit_logs=[audit_log])

    def create_rights(self):
        rights = {
            'None': 0x00,
            'Show': 0x01,
            'Create': 0x02,
            'Update': 0x04,
            'Delete': 0x08
        }
        res = list()
        for _k, _v in rights.iteritems():
            res.append(Right.insert_rights(_k, _v, self.resources))
        return res


    def create_resources(self):
        resources = {
            'User': 0xff,
            'Role': 0xff,
            'Right': 0xff,
            'Resource': 0xff,
            'Log': 0xff,
            'AuditLog': 0xff,
            'Address': 0xff,
            'Persion': 0xff
        }
        res = list()
        for _name, _weight in resources.iteritems():
            res.append(Resource.insert_resources(_name, _weight))
        return res

    def create_role(self):
        Role.insert_roles('Administrator', resources=self.resources, users=[self.user])
        Role.insert_roles('Unknow', resources=None, users=None)
        Role.insert_roles('User', resources=None, users=None)


from app import login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))