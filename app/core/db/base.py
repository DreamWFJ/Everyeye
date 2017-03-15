# -*- coding: utf-8 -*-
# ===================================
# ScriptName : base.py
# Author     : WFJ
# Email      : wfj_sc@163.com
# CreateTime : 2017-03-08 18:22
# ===================================

import six
import logging
from abc import ABCMeta, abstractmethod

class BaseDatabase(six.with_metaclass(ABCMeta)):
    _logger = logging.getLogger('apscheduler.jobstores')

    def init_db(self):
        """
        init databases
        """

        alias = ''
        self._logger = logging.getLogger('apscheduler.jobstores.%s' % alias)



    def __init__(self):
        pass

    @abstractmethod
    def connect(self):
        """
        Returns a specific job, or ``None`` if it isn't found..

        The job store is responsible for setting the ``scheduler`` and ``jobstore`` attributes of
        the returned job to point to the scheduler and itself, respectively.

        :param str|unicode job_id: identifier of the job
        :rtype: Job
        """

    @abstractmethod
    def close(self):
        """
        Close current connect
        """

    @abstractmethod
    def create_tables(self):
        """
        create some tables, nosql don't need
        """

    @abstractmethod
    def insert_test_datas(self):
        """
        insert some test datas
        """

    @abstractmethod
    def remove_all_datas(self):
        """
        remove all tables
        """

    def __repr__(self):
        return '<%s>' % self.__class__.__name__


class Datastore(object):
    def __init__(self, db):
        self.db = db

    def commit(self):
        pass

    def put(self, model):
        raise NotImplementedError

    def delete(self, model):
        raise NotImplementedError    

class SQLAlchemyDatastore(Datastore):
    def commit(self):
        self.db.session.commit()

    def put(self, model):
        self.db.session.add(model)
        return model

    def delete(self, model):
        self.db.session.delete(model)


class MongoEngineDatastore(Datastore):
    def put(self, model):
        model.save()
        return model

    def delete(self, model):
        model.delete()