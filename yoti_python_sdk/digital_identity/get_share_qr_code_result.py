# -*- coding: utf-8 -*-
from __future__ import unicode_literals

class GetShareQrCodeResult(object):

    def __init__(self, data=None):
        """
        Initializes the GetShareQrCodeResult object.

        :param data: Dictionary containing QR code data.
        :type data: dict or None
        """
        data = data or {}

        self.__id = data.get("id")
        self.__expiry = data.get("expiry")
        self.__sessionId = data.get("sessionId")
        self.__redirectUri = data.get("redirectUri")

    def to_dict(self):
        """Converts the object to a dictionary representation."""
        return {
            'id': self.__id,
            'expiry': self.__expiry,
            'sessionId': self.__sessionId,
            'redirectUri': self.__redirectUri,
        }

    @property
    def id(self):
        """Returns the QR code ID."""
        return self.__id

    @property
    def expiry(self):
        """Returns the QR code expiry."""
        return self.__expiry

    @property
    def sessionId(self):
        """Returns the session ID."""
        return self.__sessionId

    @property
    def redirectUri(self):
        """Returns the redirect URI."""
        return self.__redirectUri
