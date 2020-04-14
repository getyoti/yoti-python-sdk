# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class CreateSessionResult(object):
    """
    The response to a successful CreateSession call
    """

    def __init__(self, data=None):
        """
        :param data: the data
        :type data: dict or None
        """
        if data is None:
            data = dict()

        self.__client_session_token_ttl = data.get("client_session_token_ttl", None)
        self.__session_id = data.get("session_id", None)
        self.__client_session_token = data.get("client_session_token", None)

    @property
    def client_session_token_ttl(self):
        """
        Returns the time-to-live (TTL) for the client session
        token for the created session

        :return: the client session token TTL
        :rtype: int or None
        """
        return self.__client_session_token_ttl

    @property
    def client_session_token(self):
        """
        Returns the client session token for the created session

        :return: the client session token
        :rtype: str or None
        """
        return self.__client_session_token

    @property
    def session_id(self):
        """
        Session ID of the created session

        :return: the session ID
        :rtype: str or None
        """
        return self.__session_id
