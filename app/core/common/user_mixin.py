# -*- coding: utf-8 -*-
# ===================================
# ScriptName : user_mixin.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-28 9:36
# ===================================

import sys

class UserMixin(object):
    '''
    This provides default implementations for the methods that Flask-Login
    expects user objects to have.
    '''
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        print "haha ------------"
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def __eq__(self, other):
        '''
        Checks the equality of two `UserMixin` objects using `get_id`.
        '''
        if isinstance(other, UserMixin):
            return self.get_id() == other.get_id()
        return NotImplemented

    def __ne__(self, other):
        '''
        Checks the inequality of two `UserMixin` objects using `get_id`.
        '''
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal

    if sys.version_info[0] != 2:  # pragma: no cover
        # Python 3 implicitly set __hash__ to None if we override __eq__
        # We set it back to its default implementation
        __hash__ = object.__hash__


class AnonymousUserMixin(object):
    '''
    This is the default object for representing an anonymous user.
    '''
    @property
    def is_authenticated(self):
        return False

    @property
    def is_active(self):
        return False

    @property
    def is_anonymous(self):
        return True

    def get_id(self):
        return
    