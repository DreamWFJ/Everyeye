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


    