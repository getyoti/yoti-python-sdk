# -*- coding: utf-8 -*-
from __future__ import unicode_literals

class ReceiptResponse(object):

    def __init__(self, data=None):
        """
        :param data: the data
        :type data: dict or None
        """
        if data is None:
            data = dict()
        
        self.__id = data.get("id", None)
        self.__sessionId = data.get("sessionId", None)
        self.__timestamp = data.get("timestamp", None)
        self.__rememberMeId = data.get("rememberMeId", None)
        self.__parentRememberMeId = data.get("parentRememberMeId", None)
        self.__content = data.get("content", None)
        self.__otherPartyContent = data.get("otherPartyContent", None)
        self.__wrappedItemKeyId = data.get("wrappedItemKeyId", None)
        self.__wrappedKey = data.get("wrappedKey", None)

    def to_dict(self):
        return {
            'id': self.__id,
            'sessionId': self.__sessionId,
            'timestamp': self.__timestamp,
            'rememberMeId': self.__rememberMeId,
            'parentRememberMeId': self.__parentRememberMeId,
            'content': self.__content,
            'otherPartyContent': self.__otherPartyContent,
            'wrappedItemKeyId': self.__wrappedItemKeyId,
            'wrappedKey': self.__wrappedKey,
        }

    @property
    def id(self):
        """
        :return: the id
        :rtype: str or None
        """
        return self.__id
    
    @property
    def sessionId(self):
        """
        :return: the session id
        :rtype: str or None
        """
        return self.__sessionId
    
    @property
    def timestamp(self):
        """
        :return: the timestamp
        :rtype: str or None
        """
        return self.__timestamp
    
    @property
    def rememberMeId(self):
        """
        :return: the remember me id
        :rtype: str or None
        """
        return self.__rememberMeId
    
    @property
    def parentRememberMeId(self):
        """
        :return: the parent remember me id
        :rtype: str or None
        """
        return self.__parentRememberMeId
    
    @property
    def content(self):
        """
        :return: the content
        :rtype: str or None
        """
        return self.__content
    
    @property
    def otherPartyContent(self):
        """
        :return: the other party content
        :rtype: str or None
        """
        return self.__otherPartyContent
    
    @property
    def wrappedItemKeyId(self):
        """
        :return: the wrapped item key id
        :rtype: str or None
        """
        return self.__wrappedItemKeyId
    
    @property
    def wrappedKey(self):
        """
        :return: the wrapped key
        :rtype: str or None
        """
        return self.__wrappedKey
