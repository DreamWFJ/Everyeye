# -*- coding: utf-8 -*-
# ===================================
# ScriptName : models.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-27 15:44
# ===================================
import hashlib
import random
from app.utils import generate_uuid, get_current_0_24_time
from flask import request, url_for
from datetime import datetime
from app import sql_db as db
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer
from app.core.common.user_mixin import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import and_

class DatabaseError(Exception):
    pass
class NotFoundData(Exception):
    pass

def weight2int(v):
    if not isinstance(v, int) and isinstance(v, basestring):
        return int(v, 16)
    else:
        try:
            return int(v)
        except:
            return 0

# 建立资源与角色的多对多关系
class RolesResources(db.Model):
    __tablename__ = 'roles_resources'
    id = db.Column(db.Integer, primary_key = True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # 权重，单独为某个角色附加资源时，对资源的操作权限
    right_weight = db.Column(db.Integer, default=0x00)
    # resource = db.relationship('Resource', backref=db.backref('roles', lazy='dynamic'))
    # role = db.relationship('Role', backref=db.backref('resources', lazy='dynamic'))
    resource = db.relationship('Resource', back_populates="roles")
    role = db.relationship('Role', back_populates="resources")
    create_at = db.Column(db.DateTime, default = datetime.now)

    @staticmethod
    def delete_role_resource_by_ids(ids):
        roles_resources = RolesResources.query.filter(RolesResources.id.in_(ids))
        if roles_resources:
            for role_resource in roles_resources:
                db.session.delete(role_resource)
            db.session.commit()

    def __repr__(self):
        return '<ResourcesRoles %r>' % self.__tablename__

# 建立资源与权限的多对多关系
# resources_rights = db.Table('resources_rights',
#                   db.Column('resource_id', db.String(36), db.ForeignKey('resources.id')),
#                   db.Column('right_id', db.String(36), db.ForeignKey('rights.id')))
class ResourcesRights(db.Model):
    __tablename__ = 'resources_rights'
    id = db.Column(db.Integer, primary_key = True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resources.id'))
    right_id = db.Column(db.Integer, db.ForeignKey('rights.id'))
    resource = db.relationship('Resource', back_populates="rights")
    right = db.relationship('Right', back_populates="resources")
    create_at = db.Column(db.DateTime, default = datetime.now)

    @staticmethod
    def delete_resource_right_by_ids(ids):
        resources_rights = ResourcesRights.query.filter(ResourcesRights.id.in_(ids))
        if resources_rights:
            for resource_right in resources_rights:
                db.session.delete(resource_right)
            db.session.commit()

    def __repr__(self):
        return '<ResourcesRights %r>' % self.__tablename__

# 角色表
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    # 角色名称
    name = db.Column(db.String(64), unique = True)
    # 角色状态，表示是锁定
    status = db.Column(db.Boolean, default = False, index = True)
    # 默认角色选项
    default = db.Column(db.Boolean, default=False, index=True)

    # 与资源的多对多关系
    # resources = db.relationship('Resource',
    #                            secondary = resources_roles,
    #                            backref = db.backref('roles', lazy='dynamic'))
    # role_resources = db.relationship('RolesResources', backref = 'roles', cascade="all, delete-orphan")
    resources = db.relationship("RolesResources", back_populates="role",
                                primaryjoin="RolesResources.role_id==Role.id")
    # 与用户的一对多关系
    users = db.relationship('User', backref = 'roles', lazy = 'dynamic')
    create_at = db.Column(db.DateTime, default = datetime.now)

    def __repr__(self):
        return '<Role %r>' % self.name


    @staticmethod
    def insert_roles(rolename, status=False, role_resource=None, default=None):
        role = Role(name = rolename)
        if role_resource:
            role.resources.append(role_resource)
        if default:
            role.default = default
        db.session.add(role)
        db.session.commit()

        return role

    @staticmethod
    def set_status(role_id, status):
        # 设置角色是否被锁定
        role = Role.query.filter_by(id=role_id).first()
        if role:
            role.status = status
            db.session.add(role)
            db.session.commit()

    @staticmethod
    def set_default(role_id, status):
        # 设置默认角色
        roles = Role.query.filter_by(default = status).all()
        print list(roles)
        if roles:
            for role in roles:
                role.default = not status
                db.session.add(role)
            db.session.commit()
        role = Role.query.filter_by(id=role_id).first()
        if role:
            role.default = status
            db.session.add(role)
            db.session.commit()

    @staticmethod
    def add_resource(rolename, resourcename, weight):
        role = Role.query.filter_by(name = rolename).first()
        if role is None:
            raise NotFoundData('role name <%s> not existed.'%rolename)
        resource = Resource.query.filter_by(name=resourcename).first()
        if resource is None:
            raise NotFoundData('resource name <%s> not existed.'%resourcename)
        role_resource = RolesResources(right_weight=weight2int(weight))
        role_resource.resource = resource
        role.resources.append(role_resource)
        db.session.add(resource)
        db.session.add(role_resource)
        db.session.add(role)
        db.session.commit()

        return role

    @staticmethod
    def add_role_user_by_ids(name, user_ids):
        # 删除用户角色关系通过ID
        role = Role.query.filter_by(name = name).first()
        users = User.query.filter(User.id.in_(user_ids)).all()
        if users and role:
            for user in users:
                user.role_id = role.id
                db.session.add(user)
            db.session.commit()

    @staticmethod
    def add_role_resource_by_id(name, resource_id, weight):
        role = Role.query.filter_by(name = name).first()
        resource = Resource.query.filter_by(id=resource_id).first()
        if role and resource:
            # 这里需要判断资源的权重是否大于等于关联关系中添加的权重
            role_resource = RolesResources.query.filter(and_(RolesResources.right_weight==weight2int(weight),
                                                             RolesResources.resource_id==resource_id,
                                                             RolesResources.role_id==role.id)).first()
            if not role_resource:
                role_resource = RolesResources(right_weight=weight2int(weight))
                role_resource.resource = resource
                role.resources.append(role_resource)
                db.session.add_all([role_resource, role])
                db.session.commit()

    @staticmethod
    def delete_role(name):
        role = Role.query.filter_by(name = name).first()
        if role:
            db.session.delete(role)
            db.session.commit()

    @staticmethod
    def delete_role_by_ids(ids):
        roles = Role.query.filter(Role.id.in_(ids))
        if roles:
            for role in roles:
                db.session.delete(role)
            db.session.commit()

# 资源表
class Resource(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    weight = db.Column(db.Integer)
    # 资源是否启用的状态，默认为启用True
    status = db.Column(db.Boolean, default=True, index=True)
    # extra = db.Column(db.PickleType)
    # description = db.Column(db.Text())
    create_at = db.Column(db.DateTime, default = datetime.now)
    # rights = db.relationship('Right',
    #                            secondary=resources_rights,
    #                            backref = db.backref('resources', lazy='dynamic'))
    roles = db.relationship('RolesResources', back_populates = 'resource',
                            primaryjoin="RolesResources.resource_id==Resource.id")

    rights = db.relationship("ResourcesRights", back_populates="resource",
                             primaryjoin="ResourcesRights.resource_id==Resource.id")

    @staticmethod
    def insert_resources(name, weight, status=True):
        resource = Resource(name=name)
        resource.weight = weight2int(weight)
        resource.status = status
        db.session.add(resource)
        db.session.commit()
        return resource

    @staticmethod
    def set_status(resource_id, status):
        # 设置资源是否被锁定
        resource = Resource.query.filter_by(id=resource_id).first()
        if resource:
            resource.status = status
            db.session.add(resource)
            db.session.commit()

    @staticmethod
    def delete_resources(name):
        """
        注意：这里需要关注资源绑定的权限，角色关系
        """
        resource = Resource.query.filter_by(name = name).first()
        if resource:
            db.session.delete(resource)
            db.session.commit()

    @staticmethod
    def delete_resource_by_ids(ids):
        resources = Resource.query.filter(Resource.id.in_(ids))
        if resources:
            for resource in resources:
                db.session.delete(resource)
            db.session.commit()

    @staticmethod
    def add_resource_right_by_ids(name, right_ids):
        # 添加权限资源通过ID
        resource = Resource.query.filter_by(name = name).first()
        rights = Right.query.filter(Right.id.in_(right_ids)).all()
        if resource and rights:
            for right in rights:
                resource_right = ResourcesRights.query.filter(and_(
                    ResourcesRights.right_id == right.id,
                    ResourcesRights.resource_id == resource.id
                )).first()
                if not resource_right:
                    resource_right = ResourcesRights()
                    resource_right.right = right
                    resource.rights.append(resource_right)
                    db.session.add_all([resource_right, right])
            db.session.commit()

    @staticmethod
    def add_resource_role_by_ids(name, role_ids, weight):
        # 添加权限资源通过ID
        resource = Resource.query.filter_by(name = name).first()
        roles = Role.query.filter(Role.id.in_(role_ids)).all()
        if resource and roles:
            for role in roles:
                role_resource = RolesResources.query.filter(and_(
                    RolesResources.role_id == role.id,
                    RolesResources.resource_id == resource.id
                )).first()
                if not role_resource:
                    role_resource = RolesResources(resource=resource, right_weight=weight2int(weight))
                    role_resource.role = role
                    db.session.add(role_resource)
            db.session.commit()


    def __repr__(self):
        return '<Resource %r>' % self.name

class Right(db.Model):
    __tablename__ = 'rights'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    status = db.Column(db.Boolean, default=True, index=True)
    weight = db.Column(db.Integer, unique = True)
    create_at = db.Column(db.DateTime(), default = datetime.now)
    # 与资源的多对多关系
    resources = db.relationship("ResourcesRights", back_populates="right",
                                primaryjoin="ResourcesRights.right_id==Right.id")
    # resources = db.relationship('Resource',
    #                            secondary=resources_rights,
    #                            backref = db.backref('rights', lazy='dynamic'))

    @staticmethod
    def insert_rights(name, weight, status=True):
        right = Right.query.filter_by(name = name).first()
        if right is None:
            right = Right(name = name)
        right.weight = weight2int(weight)
        right.status = status
        db.session.add(right)
        db.session.commit()

    @staticmethod
    def set_status(right_id, status):
        # 设置权限是否被锁定
        right = Right.query.filter_by(id=right_id).first()
        if right:
            right.status = status
            db.session.add(right)
            db.session.commit()

    @staticmethod
    def add_resource(rightname, resourcename):
        right = Right.query.filter_by(name = rightname).first()
        if right is None:
            raise NotFoundData('right name <%s> not existed.'%rightname)
        resource = Resource.query.filter_by(name=resourcename).first()
        if resource is None:
            raise NotFoundData('resource name <%s> not existed.'%resourcename)
        resource_right = ResourcesRights()
        resource_right.resource = resource
        right.resources.append(resource_right)
        db.session.add(resource)
        db.session.add(resource_right)
        db.session.add(right)
        db.session.commit()

        return right

    @staticmethod
    def delete_right(name):
        right = Right.query.filter_by(name = name).first()
        if right:
            db.session.delete(right)
            db.session.commit()

    @staticmethod
    def delete_right_by_ids(ids):
        rights = Right.query.filter(Right.id.in_(ids))
        if rights:
            for right in rights:
                db.session.delete(right)
            db.session.commit()

    @staticmethod
    def add_right_resource_by_ids(name, resource_ids):
        # 添加权限资源通过ID
        right = Right.query.filter_by(name = name).first()
        resources = Resource.query.filter(Resource.id.in_(resource_ids)).all()
        if right and resources:
            for resource in resources:
                resource_right = ResourcesRights.query.filter(and_(
                    ResourcesRights.right_id == right.id,
                    ResourcesRights.resource_id == resource.id
                )).first()
                if not resource_right:
                    resource_right = ResourcesRights()
                    resource_right.resource = resource
                    right.resources.append(resource_right)
                    db.session.add_all([resource_right, right])
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
    address_name = db.Column(db.String(64), unique=True)
    address_country = db.Column(db.String(64))
    address_city = db.Column(db.String(64))
    address_detail = db.Column(db.Text())
    default = db.Column(db.Boolean(), default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def insert_address(address_name, country, city, address_detail, is_default):
        address = Address.query.filter_by(address_name = address_name).first()
        if address is None:
            address = Address(address_name = address_name)
        address.address_country = country
        address.address_city = city
        address.address_detail = address_detail
        if is_default:
            address.default = is_default
        db.session.add(address)
        db.session.commit()
        return address

    def __repr__(self):
        return '<Resource %r>' % self.name

class AuditLog(db.Model):
    """用户的登录登出审计日志"""
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key = True)
    province = db.Column(db.String(16))
    city = db.Column(db.String(16))
    detail_address = db.Column(db.Text())
    ip = db.Column(db.String(16))
    login_time = db.Column(db.DateTime(), default = datetime.now)
    last_request_time = db.Column(db.DateTime(), default = datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def insert_audit_logs(province, city, detail_address, ip, login_time = None, last_request_time=None):
        audit_logs = AuditLog(province = province, city = city, ip = ip, detail_address = detail_address)
        if login_time:
            audit_logs.login_time = login_time
        if last_request_time:
            audit_logs.last_request_time = last_request_time
        db.session.add(audit_logs)
        db.session.commit()
        return audit_logs

    @staticmethod
    def refresh_last_request_time(user_id, last_request_time):
        audit_log = AuditLog.query.filter_by(user_id = user_id).first()
        if audit_log is None:
            raise NotFoundData("database audit log lose user_id='%s' the last record."%user_id)
        audit_log.last_request_time = last_request_time
        db.session.add(audit_log)
        db.session.commit()

    def __repr__(self):
        return '<AuditLog %r>' % self.__tablename__

class ActionLog(db.Model):
    """用户的操作日志"""
    __tablename__ = 'action_logs'
    id = db.Column(db.Integer, primary_key = True)
    action = db.Column(db.String(64))
    resource = db.Column(db.String(64))
    # 操作是否成功
    status = db.Column(db.Boolean, default = True, index = True)
    # 操作详情
    detail = db.Column(db.Text())
    create_at = db.Column(db.DateTime(), default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def insert_logs(action, resource, status, detail):
        log = ActionLog(action = action, resource = resource, status = status, detail = detail)
        db.session.add(log)
        db.session.commit()
        return log

    def __repr__(self):
        return '<AuditLog %r>' % self.__tablename__

class UserChatRoom(db.Model):
    """用户加入的聊天房间"""
    __tablename__ = 'user_chat_rooms'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    chat_room_id = db.Column(db.Integer, db.ForeignKey('chat_rooms.id'))
    user = db.relationship('User', back_populates="chat_rooms")
    chat_room = db.relationship('ChatRoom', back_populates="users")
    create_at = db.Column(db.DateTime, default = datetime.now)

    @staticmethod
    def delete_role_resource_by_ids(ids):
        roles_resources = RolesResources.query.filter(RolesResources.id.in_(ids))
        if roles_resources:
            for role_resource in roles_resources:
                db.session.delete(role_resource)
            db.session.commit()

    @staticmethod
    def insert_user_chat_room(user, room):
        user_chat_room = UserChatRoom.query.filter(and_(UserChatRoom.chat_room==room, UserChatRoom.user==user)).first()
        if not user_chat_room:
            user_chat_room = UserChatRoom(user=user, chat_room=room)
            db.session.add(user_chat_room)
            db.session.commit()
        return user_chat_room

    def __repr__(self):
        return '<UserChatRoom %r>' % self.__tablename__

class ChatRoom(db.Model):
    """
    聊天房间
    """
    __tablename__ = 'chat_rooms'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    messages = db.relationship('Message', backref = 'chat_rooms', lazy = 'dynamic')
    users = db.relationship("UserChatRoom", back_populates="chat_room",
                                primaryjoin="UserChatRoom.chat_room_id==ChatRoom.id")
    # 房间是否禁言
    status = db.Column(db.Boolean(), default=False)
    default = db.Column(db.Boolean(), default=False)
    create_at = db.Column(db.DateTime, default = datetime.now)

    # 获取接受信息的用户ID和name
    def get_receivers(self, user_id):
        ret = []
        for user_chat_room in self.users:
            if user_chat_room.user_id == user_id:
                continue
            u = User.query.filter_by(id=user_chat_room.user_id).first()
            ret.append({'id':user_chat_room.user_id, 'name':u.name})
        return ret

    @staticmethod
    def insert_chat_room(name, status=False):
        chat_room = ChatRoom.query.filter_by(name=name, status=status).first()
        if not chat_room:
            chat_room = ChatRoom(name=name, status=status)
            db.session.add(chat_room)
            db.session.commit()
        return chat_room

    @staticmethod
    def send_message(room_name, message):
        chat_room = ChatRoom.query.filter_by(name=room_name).first()
        if not chat_room:
            chat_room = ChatRoom.insert_chat_room(name=room_name)
        chat_room.messages.append(message)
        db.session.add(chat_room)
        db.session.commit()

    @staticmethod
    def init():
        default_rooms = ["system_notice"]
        for room in default_rooms:
            chat_room = ChatRoom(name=room, default=True)
            db.session.add(chat_room)
        db.session.commit()


    def __repr__(self):
        return '<NoticeMessage %r >' % self.__tablename__

class Message(db.Model):
    """用户的消息记录"""
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key = True)
    subject = db.Column(db.String(64))
    content = db.Column(db.Text())
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('chat_rooms.id'))
    status = db.Column(db.Boolean(), default=False)
    # single and group
    type = db.Column(db.String(64), default='single')
    create_at = db.Column(db.DateTime(), default=datetime.now)

    @property
    def sender(self):
        return User.query.filter_by(id=self.sender_id).first().name
    @staticmethod
    def get_message_sent(user_id):
        return Message.query.filter(and_(Message.type == 'single', Message.sender_id==user_id)).all()

    @property
    def receivers(self):
        chat_room = ChatRoom.query.filter_by(id=self.room_id).first()
        if chat_room:
            return chat_room.get_receivers(self.sender_id)

    @staticmethod
    def insert_message(subject, content, message_type=None):
        message = Message(subject=subject, content=content)
        if message_type:
            message.type = message_type
        db.session.add(message)
        db.session.commit()
        return message

    def __repr__(self):
        return '<Message %r>' % self.id


class User(UserMixin, db.Model):
    """用户信息
       建议最终将各个类型业务处理单独用类实现，作为一个混合类Mixin
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    # 用户名名称
    name = db.Column(db.String(64), unique = True, index = True)
    # 真实名称
    real_name = db.Column(db.String(64))
    # 邮件地址
    email = db.Column(db.String(64), unique = True, index = True, nullable=True)
    # 手机号码
    telephone = db.Column(db.String(16), unique = True, index = True)
    password_hash = db.Column(db.String(128), nullable=True)
    # 是否激活用户，默认激活，管理员可以禁止该用户登录，通过设置该选项 --------------- 注意---------------
    status = db.Column(db.Boolean, default = True)
    # 邮件是否确认
    confirmed = db.Column(db.Boolean, default=False)
    # 角色ID
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # 个人标识符哈希值
    avatar_hash = db.Column(db.String(32))
    identity_card_number = db.Column(db.String(32))
    # 其他信息
    extra = db.Column(db.PickleType())
    # 用户文章
    articles = db.relationship('Article', backref = 'user', lazy= 'dynamic')
    # 用户创建时间
    create_at = db.Column(db.DateTime(), default = datetime.now)
    # 用户地址信息
    addresses = db.relationship('Address', backref = 'user', lazy = 'dynamic')
    # 操作日志信息
    action_logs = db.relationship('ActionLog', backref = 'user', lazy = 'dynamic')

    # 消息信息
    messages = db.relationship('Message', backref = 'user', lazy = 'dynamic')
    # 聊天房间
    chat_rooms = db.relationship("UserChatRoom", back_populates="user",
                                primaryjoin="UserChatRoom.user_id==User.id")
    # 登陆登出的审计日志信息
    audit_logs = db.relationship('AuditLog', backref = 'user', lazy = 'dynamic')
    # 用户的评论信息
    comments = db.relationship('ArticleComment', backref = 'user', lazy = 'dynamic')
    # 关于我
    about_me = db.Column(db.Text())


    def __repr__(self):
        return '<User %r>' % self.name

    def to_json(self):
        json_use = {
            'url': url_for('v1.user_api', id = self.id, _external = True),
            'id': self.id,
            'username': self.name,
            'email': self.email,
            'member_since': self.create_at.strftime('%c'),
            'articles': self.articles.count()
        }
        return json_use

    @property
    def message_received(self):
        messages = self.get_message_received(status=False)
        print "popoer message: ", messages
        return messages

    def add_message_sent(self, message):
        """添加已经发送的消息"""
        self.messages.append(message)
        db.session.add(self)
        db.session.commit()

    def add_default_room(self):
        rooms = ChatRoom.query.filter_by(default=True).all()
        if len(rooms) > 0:
            for room in rooms:
                user_chat_room = UserChatRoom(chat_room=room, user=self)
                self.chat_rooms.append(user_chat_room)
                db.session.add(self)
            db.session.commit()

    def add_to_chat_room(self, room_name):
        room = ChatRoom.insert_chat_room(room_name)
        user_chat_room = UserChatRoom.insert_user_chat_room(self, room)
        if user_chat_room not in self.chat_rooms:
            self.chat_rooms.append(user_chat_room)
            db.session.add(self)
        db.session.commit()

    def send_message(self, send_to, subject, content):
        # 发送消息
        user = User.query.filter_by(id=send_to).first()
        if user:
            room_name = "%s_%s"%(self.name, user.name)
            self.add_to_chat_room(room_name)
            user.add_to_chat_room(room_name)
            message = Message.insert_message(subject, content)
            self.add_message_sent(message)
            ChatRoom.send_message(room_name, message)

    def get_message_sent(self):
        return Message.get_message_sent(self.id)

    def get_message_received(self, status=None, message_id=None):
        """
            接收发送给自己的消息
            流程：1、检查和自己有关的房间
                 2、找到房间中的消息

        """
        ret = []
        if message_id:
            msgs = Message.query.filter_by(id=message_id).all()
            print "query by message id: ", message_id, msgs
            return msgs

        user_rooms = UserChatRoom.query.filter_by(user_id=self.id).all()
        for user_room in user_rooms:
            if status is None:
                messages = Message.query.filter(and_(Message.type == 'single',
                                                     Message.sender_id!=self.id,
                                                     Message.room_id==user_room.chat_room_id)).all()
            else:
                messages = Message.query.filter(and_(Message.type == 'single',
                                                     Message.sender_id!=self.id,
                                                     Message.status == status,
                                                     Message.room_id==user_room.chat_room_id)).order_by(Message.status.asc()).all()
            ret.extend(messages)
        return ret

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
    def insert_users(username, email, password, status=True, telephone=None, addresses=None, articles=None, action_logs=None, messages=None, audit_logs=None, is_admin=False, confirmed=False):
        """说明：该方法需要改进的地方是，通过传入用户名，邮箱，密码之后，需要为其关联普通用户角色，
        角色所能够操作的资源是预分配的"""
        user = User(name=username, email=email, password_hash=generate_password_hash(password))
        if telephone:
            user.telephone = telephone
        user.status = status
        if addresses:
            user.addresses = addresses
        if articles:
            user.articles = articles
        if action_logs:
            user.action_logs = action_logs
        if audit_logs:
            user.audit_logs = audit_logs
        if messages:
            user.messages = messages
        if confirmed:
            user.confirmed = confirmed
        if is_admin:
            user_role = Role.query.filter_by(name='Administrator').first()
        else:
            user_role = Role.query.filter_by(default=True).first()
        user.role_id = user_role.id
        db.session.add(user)
        db.session.commit()
        user.add_default_room()
        return user

    @staticmethod
    def delete_user(name):
        # 删除用户通过名称
        user = User.query.filter_by(name = name).first()
        if user:
            db.session.delete(user)
            db.session.commit()

    @staticmethod
    def delete_user_by_ids(ids):
        # 删除用户通过ID
        users = User.query.filter(User.id.in_(ids))
        if users:
            for user in users:
                db.session.delete(user)
            db.session.commit()

    @staticmethod
    def delete_user_role_by_ids(ids):
        # 删除用户角色关系通过ID
        users = User.query.filter(User.id.in_(ids))
        if users:
            for user in users:
                user.role_id = None
                db.session.add(user)
            db.session.commit()

    @staticmethod
    def set_status(user_id, status):
        # 设置用户是否被锁定
        user = User.query.filter_by(id=user_id).first()
        if user:
            user.status = status
            db.session.add(user)
            db.session.commit()

    @staticmethod
    def update_role(username, role_id):
        # 改变用户角色
        user = User.query.filter_by(name=username).first()
        if user:
            user.role_id = role_id
            db.session.add(user)
            db.session.commit()

    @staticmethod
    def add_action_log(username, action_log):
        user = User.query.filter_by(name=username).first()
        if user:
            user.action_logs.append(action_log)
            db.session.add(user)
            db.session.commit()

    @staticmethod
    def update_user(name, real_name=None, email=None, role_id=None, status=None, confirmed=None, about_me=None, identity_card_number=None, telephone=None):
        user = User.query.filter_by(name=name).first()
        if user:
            user.name = name
            if real_name:
                user.real_name = real_name
            if email:
                user.email = email
            if status:
                user.status = status
            if role_id:
                user.role_id = role_id
            if confirmed:
                user.confirmed = confirmed
            if about_me:
                user.about_me = about_me
            if identity_card_number:
                user.identity_card_number = identity_card_number
            if telephone:
                user.telephone = telephone
            db.session.add(user)
            db.session.commit()

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

    def has_right(self, res, action):
        """验证是否具有资源的某项权限，首先检查角色是否拥有该资源，其次再检查该角色绑定的资源是否拥有指定的操作"""
        right_weight = getattr(RightWeight, action.upper())
        # 首先获取资源ID
        resource_result = Resource.query.filter_by(name=res).first()
        if resource_result is None:
            return False
        # 根据角色ID和资源ID组合查询角色下是否拥有该资源
        role_res = RolesResources.query.filter_by(role_id=self.role_id, resource_id=resource_result.id).first()
        if role_res is None:
            return False
        # 对比权重
        if role_res.right_weight & right_weight == 0:
            return False
        return True

    def is_administrator(self):
        """检查是否是管理员"""
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

    def new_audit_log(self, ip):
        """产生审计日志"""
        print "user: %s, ip: %s login."%(self.name, ip)
        login_province = 'beijin'
        login_city = 'beijin'
        login_address = 'haidianqu'
        s, e = get_current_0_24_time()
        log = AuditLog.query.filter(and_(AuditLog.user_id==self.id, AuditLog.last_request_time >= s, AuditLog.last_request_time <= e)).first()
        if log is None:
            log = AuditLog.insert_audit_logs(login_province, login_city, login_address, ip)
        self.audit_logs.append(log)
        db.session.add(self)
        db.session.commit()

    def add_action_log(self, action, resource, status, detail):
        action_log = ActionLog.insert_logs(action, resource, status, detail)
        self.action_logs.append(action_log)
        db.session.add(self)
        db.session.commit()

    def refresh_last_request_time(self, last_request_time=None):
        """刷新访问时间"""
        if last_request_time is None:
            last_request_time = datetime.now()
        s, e = get_current_0_24_time()
        log = AuditLog.query.filter(and_(AuditLog.user_id==self.id, AuditLog.last_request_time >= s, AuditLog.last_request_time <= e)).first()
        if log:
            AuditLog.refresh_last_request_time(self.id, last_request_time)

    @property
    def last_visit_time(self):
        """获取最后访问时间"""
        result = AuditLog.query.filter_by(user_id=self.id).order_by(db.desc(AuditLog.last_request_time)).first()
        if result:
            return result.last_request_time
        return None

    def get_default_address(self):
        return Address.query.filter(and_(Address.user_id==self.id, Address.default==True)).first()

    def add_new_address(self, name, country, city, address_detail, is_default):
        """添加新的地址信息"""
        address = Address.insert_address(name, country, city, address_detail, is_default)
        self.addresses.append(address)
        db.session.add_all([self, address])
        db.session.commit()

    def update_address(self, name, country, city, address_detail):
        """添加新的地址信息"""
        address = Address.query.filter(and_(Address.user_id==self.id, Address.default==True)).first()
        if address:
            address.city = city
            address.country = country
            address.address_detail = address_detail
            db.session.add(address)
            db.session.commit()

    def delete_address(self, name):
        """删除地址信息， 后期需要做到删除后让重新设置一个默认地址"""
        address = Address.query.filter(and_(Address.user_id==self.id, Address.default==True)).first()
        if address:
            db.session.delete(address)
            db.session.commit()

class AnonymousUser(AnonymousUserMixin):
    def is_administrator(self):
        return False

    def has_right(self, res, action):
        return False

class ArticleCommentFollow(db.Model):
    __tablename__ = 'article_comment_follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('article_comments.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('article_comments.id'),
                            primary_key=True)
    create_at = db.Column(db.DateTime, default = datetime.now)

    def __repr__(self):
        return '<ArticleCommentFollow follower_id: %r, followed_id: %r >' % (self.follower_id, self.followed_id)

class ArticleComment(db.Model):
    """文章评论信息"""
    __tablename__ = 'article_comments'
    id = db.Column(db.Integer, primary_key = True)
    # 写评论的用户
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    # 评论状态，是否锁定
    status = db.Column(db.Boolean(), default=False)
    # 评论内容
    content = db.Column(db.Text())
    comment_type = db.Column(db.String(64), default='comment')
    # 评论时间
    create_at = db.Column(db.DateTime, default = datetime.now)
    # 表示我评论谁
    followed = db.relationship('ArticleCommentFollow',
                               foreign_keys=[ArticleCommentFollow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    # 表示谁评论我(这里的我表示写评论的用户)
    followers = db.relationship('ArticleCommentFollow',
                                foreign_keys=[ArticleCommentFollow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    @property
    def is_reply(self):
        return False if self.followed.count() == 0 else True

    @property
    def followed_name(self):
        if self.is_reply:
            user_id = self.followed.first().followed.user_id
            return User.query.filter_by(id=user_id).first().name

    @property
    def user_name(self):
        return User.query.filter_by(id=self.user_id).first().name

    @property
    def user_avatar(self):
        return User.query.filter_by(id=self.user_id).first().gravatar(size=256)

    @staticmethod
    def get_article_comments(article_id):
        all_comments = []
        article_comments = ArticleComment.query \
            .filter(and_(ArticleComment.comment_type=="comment",
                         ArticleComment.article_id==article_id)) \
            .order_by(ArticleComment.create_at.asc()).all()

        for comment in article_comments:
            all_comments.append(comment)
            follower_ids = [one.follower_id for one in comment.followers.all()]
            if len(follower_ids) > 0:
                article_reply_comments = ArticleComment.query \
                    .filter(and_(ArticleComment.comment_type=="reply",
                                 ArticleComment.id.in_(follower_ids))) \
                    .order_by(ArticleComment.create_at.asc()).all()

                for article_reply_comment in article_reply_comments:
                    all_comments.append(article_reply_comment)
                    follower_ids = [one.follower_id for one in article_reply_comment.followers.all()]
                    if len(follower_ids) > 0:
                        article_reply_to_reply_comments = ArticleComment \
                            .query.filter(and_(ArticleComment.comment_type=="reply",
                                               ArticleComment.id.in_(follower_ids))) \
                            .order_by(ArticleComment.create_at.asc()).all()
                        all_comments.extend(article_reply_to_reply_comments)

        return all_comments
        # return ArticleComment.query.filter_by(article_id=article_id).order_by(ArticleComment.comment_type.asc(), ArticleComment.create_at.asc()).all()

    @staticmethod
    def add_comment(user_id, article_id, content):
        article = Article.query.filter_by(id=article_id).first()
        user = User.query.filter_by(id=user_id).first()
        if article and user:
            comment = ArticleComment(user=user, article=article, content=content)
            db.session.add(comment)
            db.session.commit()

    @staticmethod
    def add_reply(user_id, reply_to_comment_id, article_id, content):
        # user_id 是指谁在写评论，reply_to_user_id 是评论谁
        article = Article.query.filter_by(id=article_id).first()
        user = User.query.filter_by(id=user_id).first()
        if article and user:
            followed = ArticleComment.query.filter_by(id=reply_to_comment_id).first()
            if followed:
                comment = ArticleComment(user=user, article=article, content=content, comment_type="reply")
                article_comment_follow = ArticleCommentFollow(follower=comment, followed=followed)
                db.session.add(article_comment_follow)
                db.session.commit()

    def __repr__(self):
        return '<ArticleComment user_id: %r, article_id: %r >' % (self.user_id, self.article_id)

class ArticleSource(db.Model):
    """文章来源信息"""
    __tablename__ = 'article_sources'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique=True)
    status = db.Column(db.Boolean(), default=False)
    articles = db.relationship('Article', backref = 'article_sources', lazy = 'dynamic')
    create_at = db.Column(db.DateTime, default = datetime.now)

    @staticmethod
    def insert_source(name, status=False):
        article_source = ArticleSource.query.filter_by(name = name).first()
        if article_source is None:
            article_source = ArticleSource(name = name, status = status)
            db.session.add(article_source)
            db.session.commit()

    @staticmethod
    def init():
        sources = ["original", "quote", "other"]
        for source in sources:
            ArticleSource.insert_source(source)

    def __repr__(self):
        return '<ArticleSource %r>' % self.name

class ArticleCategory(db.Model):
    """文章来源信息"""
    __tablename__ = 'article_categorys'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique=True)
    status = db.Column(db.Boolean(), default=False)
    articles = db.relationship('Article', backref = 'article_categorys', lazy = 'dynamic')
    create_at = db.Column(db.DateTime, default = datetime.now)

    @staticmethod
    def insert_categorys(categorys):
        for category in categorys:
            article_category = ArticleCategory.query.filter_by(name = category).first()
            if article_category is None:
                article_source = ArticleCategory(name = category)
                db.session.add(article_source)
        db.session.commit()

    @staticmethod
    def insert_category(name, status):
        article_category = ArticleCategory.query.filter_by(name = name).first()
        if article_category is None:
            article_source = ArticleCategory(name = name, status = status)
            db.session.add(article_source)
        db.session.commit()

    @staticmethod
    def init():
        article_categorys = ["work", "learning", "life", "other"]
        ArticleCategory.insert_categorys(article_categorys)

    def __repr__(self):
        return '<ArticleCategory %r>' % self.name

# 建立文章与关键词的多对多关系
# article_keywords = db.Table('article_keywords',
#                             db.Column('keyword_id', db.String(36), db.ForeignKey('article_keyword.id')),
#                             db.Column('article_id', db.String(36), db.ForeignKey('articles.id')))

class ArticleKeywords(db.Model):
    __tablename__ = 'article_keywords'
    id = db.Column(db.Integer, primary_key = True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    keyword_id = db.Column(db.Integer, db.ForeignKey('keywords.id'))
    article = db.relationship('Article', back_populates="keywords")
    keyword = db.relationship('Keyword', back_populates="articles")
    create_at = db.Column(db.DateTime, default = datetime.now)

    @staticmethod
    def delete_article_keyword_by_ids(ids):
        resources_rights = ResourcesRights.query.filter(ResourcesRights.id.in_(ids))
        if resources_rights:
            for resource_right in resources_rights:
                db.session.delete(resource_right)
            db.session.commit()

    def __repr__(self):
        return '<ArticleKeywords %r>' % self.__tablename__

class Keyword(db.Model):
    """文章关键词"""
    __tablename__ = 'keywords'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique=True)
    status = db.Column(db.Boolean(), default=False)
    color = db.Column(db.String(64))
    create_at = db.Column(db.DateTime, default = datetime.now)
    articles = db.relationship("ArticleKeywords", back_populates="keyword",
                               primaryjoin="ArticleKeywords.keyword_id==Keyword.id")
    @staticmethod
    def insert_keywords(keywords):
        for keyword in keywords:
            article_keyword = Keyword.query.filter_by(name = keyword["name"]).first()
            if article_keyword is None:
                article_keyword = Keyword(name = keyword["name"])
                article_keyword.color = keyword["color"]
                db.session.add(article_keyword)
        db.session.commit()

    @staticmethod
    def insert_keyword(name, color, status=True):
        article_keyword = Keyword.query.filter_by(name = name).first()
        if article_keyword is None:
            article_keyword = Keyword(name = name, color = color, status = status)
            db.session.add(article_keyword)
        db.session.commit()
        return article_keyword

    @staticmethod
    def delete_keyword(name):
        keyword = Keyword.query.filter_by(name = name).first()
        if keyword:
            db.session.delete(keyword)
            db.session.commit()

    @staticmethod
    def delete_keyword_by_ids(ids):
        keywords = Keyword.query.filter(Keyword.id.in_(ids))
        if keywords:
            for keyword in keywords:
                db.session.delete(keyword)
            db.session.commit()

    @staticmethod
    def init():
        article_keywords = [
            {
                "id":1, "name":"Aritcle", "color":"default"
            },
            {
                "id":2, "name":"nothing", "color":"primary"
            },
            {
                "id":3, "name":"learning", "color":"success"
            },
            {
                "id":4, "name":"CDN", "color":"info"
            },
            {
                "id":5, "name":"K8S", "color":"warning"
            },
            {
                "id":6, "name":"Cloud", "color":"danger"
            },
            {
                "id":7, "name":"mouse", "color":"default"
            },
            {
                "id":8, "name":"apple", "color":"primary"
            }
        ]
        Keyword.insert_keywords(article_keywords)

    def __repr__(self):
        return '<ArticleKeyword %r>' % self.name


class ArticleContentType(db.Model):
    """文章内容类型"""
    __tablename__ = 'article_content_types'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique=True)
    status = db.Column(db.Boolean(), default=False)
    create_at = db.Column(db.DateTime, default = datetime.now)

    @staticmethod
    def insert_content_types(content_types):
        for content_type in content_types:
            article_content_type = ArticleContentType.query.filter_by(name = content_type).first()
            if article_content_type is None:
                article_content_type = ArticleContentType(name = content_type)
                db.session.add(article_content_type)
        db.session.commit()

    @staticmethod
    def init():
        content_types = ["summernote", "markdown"]
        ArticleContentType.insert_content_types(content_types)

    def __repr__(self):
        return '<ArticleContentType %r>' % self.name

class ArticleReferenceLink(db.Model):
    """文章参考链接"""
    __tablename__ = 'article_reference_links'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    create_at = db.Column(db.DateTime, default = datetime.now)
    status = db.Column(db.Boolean(), default=False)

    @staticmethod
    def insert_reference_links(reference_links):
        # 插入多个链接，json格式
        for reference_link in reference_links:
            article_reference_link = ArticleReferenceLink.query.filter_by(name = reference_link).first()
            if article_reference_link is None:
                article_reference_link = ArticleReferenceLink(name = reference_link)
                db.session.add(article_reference_link)
        db.session.commit()

    @staticmethod
    def insert_reference_link(reference_link):
        # 插入单个参考链接
        article_reference_link = ArticleReferenceLink.query.filter_by(name = reference_link).first()
        if article_reference_link is None:
            article_reference_link = ArticleReferenceLink(name = reference_link)
            db.session.add(article_reference_link)
        db.session.commit()
        return article_reference_link

    @staticmethod
    def update_reference_link(article_id, reference_links):
        # 更新文章的参考链接
        return_reference_link = []
        ArticleReferenceLink.remove_reference_link_by_article_id(article_id)
        if reference_links:
            for reference_link in reference_links:
                if len(reference_link) == 0:
                    continue
                article_reference_link = ArticleReferenceLink.query.filter_by(article_id=article_id, name = reference_link).first()
                if article_reference_link is None:
                    article_reference_link = ArticleReferenceLink(article_id=article_id, name = reference_link)
                    db.session.add(article_reference_link)
                return_reference_link.append(article_reference_link)
        db.session.commit()
        return return_reference_link
    @staticmethod
    def remove_reference_link_by_ids(ids):
        # 通过ID删除参考链接
        article_reference_links = ArticleReferenceLink.query.filter(ArticleReferenceLink.id.in_(ids))
        if article_reference_links:
            for article_reference_link in article_reference_links:
                db.session.delete(article_reference_link)
            db.session.commit()

    @staticmethod
    def remove_reference_link_by_article_id(article_id):
        article_reference_links = ArticleReferenceLink.query.filter_by(article_id=article_id).all()
        if article_reference_links:
            for article_reference_link in article_reference_links:
                db.session.delete(article_reference_link)
            db.session.commit()

    def __repr__(self):
        return '<ArticleReferenceLink %r>' % self.name

class ArticleViewRecord(db.Model):
    """文章访问记录"""
    __tablename__ = 'article_view_records'
    id = db.Column(db.Integer, primary_key = True)
    ip = db.Column(db.String(64))
    user_id = db.Column(db.Integer)
    status = db.Column(db.Boolean(), default=False)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    create_at = db.Column(db.DateTime, default = datetime.now)

    @staticmethod
    def insert_content_types(view_records):
        for view_record in view_records:
            article_view_record = ArticleViewRecord.query.filter_by(name = view_record).first()
            if article_view_record is None:
                article_view_record = ArticleViewRecord(name = view_record)
                db.session.add(article_view_record)
        db.session.commit()

    def __repr__(self):
        return '<ArticleViewRecord %r>' % self.name

class Article(db.Model):
    """文章信息"""
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key = True)
    # 文章作者
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # 文章标题
    title = db.Column(db.String(64), unique=True)
    # 文章关键词
    keywords = db.relationship('ArticleKeywords',
                               back_populates="article",
                               primaryjoin="ArticleKeywords.article_id==Article.id")

    # 文章来源
    source_id = db.Column(db.Integer, db.ForeignKey('article_sources.id'))
    # 文章目录
    category_id = db.Column(db.Integer, db.ForeignKey('article_categorys.id'))
    # 文章状态，是否被锁定
    status = db.Column(db.Boolean(), default=False)
    # 文章是否允许被评论
    permit_comment = db.Column(db.Boolean(), default=False)
    # 文章图像名称
    image_name = db.Column(db.String(64), default=None)
    # 文章内容
    content = db.Column(db.Text())
    # 文章内容类型，目前支持富文本和markdown
    # content_type_id = db.Column(db.Integer, db.ForeignKey('article_content_types.id'))
    content_type = db.Column(db.String(64))
    # 文章中参考的链接
    reference_links = db.relationship('ArticleReferenceLink', backref = 'articles', lazy = 'dynamic')
    # 发表时间
    public_time = db.Column(db.DateTime, default = datetime.now)
    # 文章修改时间
    change_time = db.Column(db.DateTime)
    # 文章访问信息
    views = db.relationship('ArticleViewRecord', backref = 'article', lazy = 'dynamic')
    # 文章评论信息
    comments = db.relationship('ArticleComment', backref = 'article', lazy= 'dynamic')

    @property
    def author(self):
        # 获取文章作者
        user = User.query.filter_by(id=self.user_id).first()
        return user.name

    @staticmethod
    def get_keyword_color():
        keyword_color_dict = {
            "1":"default",
            "2":"primary",
            "3":"success",
            "4":"info",
            "5":"warning",
            "6":"danger"
        }
        return random.choice(keyword_color_dict.values())

    @staticmethod
    def insert_article(user_id, title, keywords, source_id, category_id, status, permit_comment, image_name, content, content_type, reference_links):
        article = Article(user_id = user_id,
                          title = title,
                          source_id = source_id,
                          category_id = category_id,
                          permit_comment = permit_comment,
                          image_name = image_name,
                          status = status,
                          content = content,
                          content_type = content_type)
        keyword_list = keywords.split(',')
        if len(keyword_list) > 0:
            for keyword in keyword_list:
                keyword = Keyword.insert_keyword(keyword, Article.get_keyword_color())
                article_keyword = ArticleKeywords.query.filter(and_(ArticleKeywords.article_id==article.id, ArticleKeywords.keyword_id==keyword.id)).first()
                if not article_keyword:
                    article_keyword = ArticleKeywords(article=article, keyword=keyword)
                article.keywords.append(article_keyword)
                db.session.add(article_keyword)

        if len(reference_links) > 0:
            for reference_link in reference_links:
                if len(reference_link) == 0:
                    continue
                article_reference_link = ArticleReferenceLink.query.filter_by(name = reference_link).first()
                if article_reference_link is None:
                    article_reference_link = ArticleReferenceLink(name = reference_link)
                    db.session.add(article_reference_link)
                article.reference_links.append(article_reference_link)
        else:
            article.reference_links = None
        db.session.add(article)
        db.session.commit()

    @staticmethod
    def update_article(article_id, title, keywords, source_id, category_id, status, permit_comment, image_name, content, content_type, reference_links):
        article = Article.query.filter_by(id=article_id).first()
        if article:
            article.title = title
            article.source_id = source_id
            article.category_id = category_id
            article.status = status
            article.permit_comment = permit_comment
            article.image_name = image_name
            article.content = content
            article.content_type = content_type

            keyword_list = keywords.split(',')
            if len(keyword_list) > 0:
                for keyword in keyword_list:
                    keyword = Keyword.insert_keyword(keyword, Article.get_keyword_color())
                    article_keyword = ArticleKeywords.query.filter(and_(ArticleKeywords.article_id==article.id, ArticleKeywords.keyword_id==keyword.id)).first()
                    if not article_keyword:
                        article_keyword = ArticleKeywords(article=article, keyword=keyword)
                    article.keywords.append(article_keyword)
                    db.session.add(article_keyword)

            if len(reference_links) > 0:
                article_reference_links = ArticleReferenceLink.update_reference_link(article_id, reference_links)
                article.reference_links = article_reference_links
            else:
                ArticleReferenceLink.remove_reference_link_by_article_id(article_id)
                article.reference_links = None
            db.session.add(article)
            db.session.commit()

    @staticmethod
    def delete_article(name):
        article = Article.query.filter_by(name = name).first()
        if article:
            db.session.delete(article)
            db.session.commit()

    @staticmethod
    def delete_article_by_ids(ids):
        articles = Article.query.filter(Article.id.in_(ids))
        if articles:
            for article in articles:
                db.session.delete(article)
            db.session.commit()

    def __repr__(self):
        return '<Article title %r>' % self.title

# 初始化测试数据
class InitData(object):
    """初始化数据库"""
    def __init__(self):
        self.init_dict()
        self.resources = self.create_resources()
        self.create_rights()
        self.create_role()
        self.user = self.create_user()
        self.create_a_test_user()



    def init_dict(self):
        # 初始化字典数据
        ArticleContentType.init()
        ArticleSource.init()
        ArticleCategory.init()
        Keyword.init()
        ChatRoom.init()


    def create_article(self):
        pass

    def create_log(self, action, resource, detail, status=True):
        return ActionLog.insert_logs(action, resource, status, detail)

    def create_message(self):
        message =  Message.insert_message('test', "this is a test message", 'group')
        ChatRoom.send_message('system_notice', message)
        return message
    def create_message_to_wfj(self):
        message =  Message.insert_message('test1', "this is a test message to wfj")
        ChatRoom.send_message('admin_wfj', message)
        return message

    def create_address(self):
        name = 'my home'
        country = 'China'
        city = 'Beijin'
        address_detail= 'Chao yang country, Beijin, China'
        return Address.insert_address(name, country, city, address_detail, True)

    def create_audit_log(self):
        login_province = 'Beijin'
        login_city = 'Beijin'
        login_address = 'Beijin of China, chao yang country'
        ip = '192.168.1.123'
        login_time = datetime.now()
        logout_time = datetime.now()
        return AuditLog.insert_audit_logs(login_province, login_city, login_address, ip, login_time, logout_time)

    def create_user(self):
        username = 'Administrator'
        email = 'admin@163.com'
        password = 'this_is_a_test_account'
        telephone = '13641361488'
        address = self.create_address()
        log = self.create_log(action = 'update',
                              resource = 'user',
                              status = True,
                              detail = 'update user<id=1, name="haha"> to user<id=1, name="lala">, result: successful operation')
        log1 = self.create_log(action = 'create',
                              resource = 'role',
                              status = False,
                              detail = 'create role<id=1, name="haha"> to role<id=1, name="lala">, result: successful operation')
        message = self.create_message()
        message1 = self.create_message_to_wfj()
        audit_log = self.create_audit_log()
        return User.insert_users(username, email, password, telephone=telephone,
                                 addresses=[address], action_logs=[log,log1], messages=[message, message1], audit_logs=[audit_log], is_admin=True, confirmed=True)
    def create_a_test_user(self):
        wfj = User.insert_users('wfj', 'wfj@163.com', 'test', status=False, confirmed=True)
        wfj.add_to_chat_room('admin_wfj')
        haha = User.insert_users('haha', 'haha@163.com', 'test', status=True, confirmed=True)
        haha.add_to_chat_room('admin_haha')
        User.insert_users('jj', 'jj@163.com', 'test', status=True, confirmed=True)
        User.insert_users('da', 'da@163.com', 'test', status=False, confirmed=True)
        User.insert_users('fafa', 'fafa@163.com', 'test', status=True, confirmed=True)
        test = User.insert_users('test', 'test@163.com', 'test')
        test.add_to_chat_room('admin_test')
        return test


    def create_rights(self):
        rights = {
            'None': 0x00,
            'Show': 0x01,
            'Create': 0x02,
            'Update': 0x04,
            'Delete': 0x08
        }
        none = Right.insert_rights('None', 0x00)
        show = Right.insert_rights('Show', 0x01)
        create = Right.insert_rights('Create', 0x02)
        update = Right.insert_rights('Update', 0x04)
        delete = Right.insert_rights('Delete', 0x08)
        Right.add_resource('Show', 'user')
        Right.add_resource('Show', 'role')
        Right.add_resource('Show', 'right')
        Right.add_resource('Show', 'resource')
        Right.add_resource('Create', 'user')
        Right.add_resource('Create', 'role')
        Right.add_resource('Create', 'right')
        Right.add_resource('Create', 'resource')
        Right.add_resource('Update', 'user')
        Right.add_resource('Update', 'role')
        Right.add_resource('Update', 'right')
        Right.add_resource('Update', 'resource')
        Right.add_resource('Delete', 'user')
        Right.add_resource('Delete', 'role')
        Right.add_resource('Delete', 'right')
        Right.add_resource('Delete', 'resource')


    def create_resources(self):
        resources = {
            'user': 0xff,
            'role': 0xff,
            'right': 0xff,
            'resource': 0xff,
            'log': 0xff,
            'audit_log': 0xff,
            'address': 0xff,
            'email': 0xff,
            'profile': 0xff,
            'message': 0xff,
            'manage': 0xff, #管理能力，这是先觉条件，然后在看看是否有操作资源的权限
            'persion': 0xff
        }
        res = dict()
        for _name, _weight in resources.iteritems():
            res[_name] = Resource.insert_resources(_name, _weight)
        return res



    def create_role(self):
        admin = Role.insert_roles('Administrator')
        Role.add_resource('Administrator', 'user', 0xff)
        Role.add_resource('Administrator', 'role', 0xff)
        Role.add_resource('Administrator', 'right', 0xff)
        Role.add_resource('Administrator', 'resource', 0xff)
        Role.add_resource('Administrator', 'log', 0xff)
        Role.add_resource('Administrator', 'audit_log', 0xff)
        Role.add_resource('Administrator', 'address', 0xff)
        Role.add_resource('Administrator', 'email', 0xff)
        Role.add_resource('Administrator', 'persion', 0xff)
        Role.add_resource('Administrator', 'manage', 0xff)
        Role.add_resource('Administrator', 'message', 0xff)
        Role.add_resource('Administrator', 'profile', 0xff)
        unknow = Role.insert_roles('Unknow')
        user = Role.insert_roles('User', default=True)
        Role.add_resource('User', 'log', 0x01)
        Role.add_resource('User', 'address', 0x01)
        Role.add_resource('User', 'persion', 0x01)
        Role.add_resource('User', 'profile', 0x01)



from app import login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
