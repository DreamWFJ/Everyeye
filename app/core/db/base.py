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

class DB(six.with_metaclass(ABCMeta)):
    _logger = logging.getLogger('apscheduler.jobstores')

    def start(self, scheduler, alias):
        """
        Called by the scheduler when the scheduler is being started or when the job store is being
        added to an already running scheduler.

        :param apscheduler.schedulers.base.BaseScheduler scheduler: the scheduler that is starting
            this job store
        :param str|unicode alias: alias of this job store as it was assigned to the scheduler
        """

        self._scheduler = scheduler
        self._alias = alias
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

    def __repr__(self):
        return '<%s>' % self.__class__.__name__


    