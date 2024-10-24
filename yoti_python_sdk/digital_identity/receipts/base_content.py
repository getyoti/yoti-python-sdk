# -*- coding: utf-8 -*-
from __future__ import unicode_literals

class BaseContent():

    def __init__(self, extra_data=None):
        """
        :param data: the extra data
        :type data: dict or None
        """

        if extra_data is None:
            extra_data = dict()

        self.__extra_data = extra_data

    def to_dict(self):
        return {
            'extra_data': self.__extra_data,
        }

    @property
    def extra_data(self):
        """
        :return: the extra data
        :rtype: dict
        """
        return self.__extra_data
   