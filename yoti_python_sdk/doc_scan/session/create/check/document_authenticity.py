# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.doc_scan.constants import ID_DOCUMENT_AUTHENTICITY
from yoti_python_sdk.utils import YotiSerializable
from .requested_check import RequestedCheck


class RequestedDocumentAuthenticityCheckConfig(YotiSerializable):
    """
    The configuration applied when creating a Document Authenticity Check
    """

    def to_json(self):
        return {}


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
        return ID_DOCUMENT_AUTHENTICITY

    @property
    def config(self):
        return self.__config


class RequestedDocumentAuthenticityCheckBuilder(object):
    """
    Builder to assist creation of :class:`RequestedDocumentAuthenticityCheck`
    """

    @staticmethod
    def build():
        config = RequestedDocumentAuthenticityCheckConfig()
        return RequestedDocumentAuthenticityCheck(config)
