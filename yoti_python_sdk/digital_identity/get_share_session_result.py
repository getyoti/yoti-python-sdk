# -*- coding: utf-8 -*-
from __future__ import unicode_literals

class GetShareSessionResult(object):

    def __init__(self, data=None):
        """
        :param data: the data
        :type data: dict or None
        """
        self.__data = data if data is not None else {}

        self.__id = self.__data.get("id")
        self.__status = self.__data.get("status")
        self.__created = self.__data.get("created")
        self.__updated = self.__data.get("updated")
        self.__expiry = self.__data.get("expiry")
        self.__qrCode = self.__data.get("qrCode")
        self.__receipt = self.__data.get("receipt")

    def to_dict(self):
        return {
            'id': self.__id,
            'status': self.__status,
            'created': self.__created,
            'updated': self.__updated,
            'expiry': self.__expiry,
            'qrCode': self.__qrCode,
            'receipt': self.__receipt,
        }

    @property
    def id(self):
        """Returns the session ID."""
        return self.__id

    @property
    def status(self):
        """Returns the session status."""
        return self.__status

    @property
    def created(self):
        """Returns the session creation timestamp."""
        return self.__created

    @property
    def updated(self):
        """Returns the session last updated timestamp."""
        return self.__updated

    @property
    def expiry(self):
        """Returns the session expiry timestamp."""
        return self.__expiry

    @property
    def qrCode(self):
        """Returns the QR code data."""
        return self.__qrCode

    @property
    def qrCodeId(self):
        """Returns the QR code ID, if available."""
        return self.__qrCode.get("id") if self.__qrCode else None

    @property
    def receipt(self):
        """Returns the receipt data."""
        return self.__receipt

    @property
    def receiptId(self):
        """Returns the receipt ID, if available."""
        return self.__receipt.get("id") if self.__receipt else None
