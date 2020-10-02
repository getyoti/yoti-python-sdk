# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.doc_scan import constants
from yoti_python_sdk.utils import YotiSerializable, remove_null_values
from .requested_check import RequestedCheck


class RequestedDocumentAuthenticityCheckConfig(YotiSerializable):
    """
    The configuration applied when creating a Document Authenticity Check
    """

    def __init__(self, manual_check=None):
        """
        :param manual_check: the manual check value
        :type manual_check: str
        """
        self.__manual_check = manual_check

    @property
    def manual_check(self):
        """
        Returns a value for a manual check for a given
        Authenticity Check

        :return: the manual check value
        :rtype: str
        """
        return self.__manual_check

    def to_json(self):
        return remove_null_values({"manual_check": self.manual_check})


class RequestedDocumentAuthenticityCheck(RequestedCheck):
    """
    Requests creation of a Document Authenticity Check
    """

    def __init__(self, config):
        """
        :param config: the requested document authenticity check configuration
        :type config: RequestedDocumentAuthenticityCheckConfig
        """
        self.__config = config

    @property
    def type(self):
        return constants.ID_DOCUMENT_AUTHENTICITY

    @property
    def config(self):
        return self.__config


class RequestedDocumentAuthenticityCheckBuilder:
    """
    Builder to assist creation of :class:`RequestedDocumentAuthenticityCheck`
    """

    def __init__(self):
        self.__manual_check = None

    def with_manual_check_always(self):
        """
        :return: the builder
        :rtype: RequestedDocumentAuthenticityCheckBuilder
        """
        self.__manual_check = constants.ALWAYS
        return self

    def with_manual_check_fallback(self):
        """
        :return: the builder
        :rtype: RequestedDocumentAuthenticityCheckBuilder
        """
        self.__manual_check = constants.FALLBACK
        return self

    def with_manual_check_never(self):
        """
        :return: the builder
        :rtype: RequestedDocumentAuthenticityCheckBuilder
        """
        self.__manual_check = constants.NEVER
        return self

    def build(self=None):
        if self is None:
            manual_check = None
        else:
            manual_check = self.__manual_check

        config = RequestedDocumentAuthenticityCheckConfig(manual_check)
        return RequestedDocumentAuthenticityCheck(config)
