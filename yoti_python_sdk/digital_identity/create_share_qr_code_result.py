# -*- coding: utf-8 -*-
from __future__ import unicode_literals

class CreateShareQrCodeResult(object):

    def __init__(self, data=None):
        """
        :param data: the data
        :type data: dict or None
        """
        if data is None:
            data = dict()

        self.__id = data.get("id", None)
        self.__uri = data.get("uri", None)

    def to_dict(self):
        return {
            'id': self.__id,
            'uri': self.__uri,
        }

    @property
    def id(self):
        """
        :return: the qr code id
        :rtype: str or None
        """
        return self.__id
    
    @property
    def uri(self):
        """
        :return: the qr code uri
        :rtype: str or None
        """
        return self.__uri
    