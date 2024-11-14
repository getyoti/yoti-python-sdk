# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class ReceiptItemKeyResponse:
    def __init__(self, data=None):
        """
        Initializes the ReceiptItemKeyResponse with provided data.

        :param data: The data containing id, iv, and value
        :type data: dict or None
        """
        self.__id = data.get("id") if data else None
        self.__iv = data.get("iv") if data else None
        self.__value = data.get("value") if data else None

    def to_dict(self):
        """Returns the object data as a dictionary."""
        return {
            'id': self.__id,
            'iv': self.__iv,
            'value': self.__value,
        }

    @property
    def id(self):
        """Returns the id."""
        return self.__id

    @property
    def iv(self):
        """Returns the iv."""
        return self.__iv

    @property
    def value(self):
        """Returns the value."""
        return self.__value
