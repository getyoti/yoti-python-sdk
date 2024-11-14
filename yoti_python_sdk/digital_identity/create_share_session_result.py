# -*- coding: utf-8 -*-
from __future__ import unicode_literals

class CreateShareSessionResult(object):

    def __init__(self, data=None):
        """
        :param data: the data
        :type data: dict or None
        """
        if data is None:
            data = dict()

        self.__id = data.get("id", None)
        self.__status = data.get("status", None)
        self.__expiry = data.get("expiry", None)

    def to_dict(self):
        return {
            'id': self.__id,
            'status': self.__status,
            'expiry': self.__expiry,
        }

    @property
    def id(self):
        """
        :return: the session id
        :rtype: str or None
        """
        return self.__id
    
    @property
    def status(self):
        """
        :return: the session status
        :rtype: str or None
        """
        return self.__status
    
    @property
    def expiry(self):
        """
        :return: the session expiry
        :rtype: str or None
        """
        return self.__expiry
    