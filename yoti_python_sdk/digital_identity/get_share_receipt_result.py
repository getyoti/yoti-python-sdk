# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .receipts.receipt_response import ReceiptResponse
from .receipts.user_content import UserContent

class GetShareReceiptResult(ReceiptResponse):

    def __init__(self, receipt_response: ReceiptResponse, user_content: UserContent = None):
        """
        :param receipt_response: the receipt response
        :type receipt_response: ReceiptResponse
        :param user_content: the user content, defaults to a new UserContent if None
        :type user_content: UserContent or None
        """
        self.__userContent = user_content if user_content is not None else UserContent()

        self.__id = receipt_response.id
        self.__sessionId = receipt_response.sessionId
        self.__timestamp = receipt_response.timestamp
        self.__rememberMeId = receipt_response.rememberMeId
        self.__parentRememberMeId = receipt_response.parentRememberMeId

    def to_dict(self):
        return {
            'id': self.__id,
            'sessionId': self.__sessionId,
            'timestamp': self.__timestamp,
            'rememberMeId': self.__rememberMeId,
            'parentRememberMeId': self.__parentRememberMeId,
        }

    @property
    def receiptId(self):
        """Returns the receipt ID."""
        return self.__id

    @property
    def sessionId(self):
        """Returns the session ID."""
        return self.__sessionId

    @property
    def timestamp(self):
        """Returns the timestamp."""
        return self.__timestamp

    @property
    def rememberMeId(self):
        """Returns the remember me ID."""
        return self.__rememberMeId

    @property
    def parentRememberMeId(self):
        """Returns the parent remember me ID."""
        return self.__parentRememberMeId

    @property
    def userContent(self):
        """Returns the user content."""
        return self.__userContent

    @property
    def profile(self):
        """Returns the user's profile."""
        return self.__userContent.profile if self.__userContent else None

    @property
    def extra_data(self):
        """Returns the extra data."""
        return self.__userContent.extra_data if self.__userContent else {}
