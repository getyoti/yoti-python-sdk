# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.doc_scan.constants import ID_DOCUMENT_COMPARISON
from yoti_python_sdk.utils import YotiSerializable
from .requested_check import RequestedCheck


class RequestedIDDocumentComparisonCheckConfig(YotiSerializable):
    """
    The configuration applied when creating a Document Comparison Check
    """

    def to_json(self):
        return {}


class RequestedIDDocumentComparisonCheck(RequestedCheck):
    """
    Requests creation of a Document Comparison Check
    """

    def __init__(self, config):
        """
        :param config: the requested document Comparison check configuration
        :type config: RequestedIDDocumentComparisonCheckConfig
        """
        self.__config = config

    @property
    def type(self):
        return ID_DOCUMENT_COMPARISON

    @property
    def config(self):
        return self.__config


class RequestedIDDocumentComparisonCheckBuilder(object):
    """
    Builder to assist creation of :class:`RequestedIDDocumentComparisonCheck`
    """

    @staticmethod
    def build():
        config = RequestedIDDocumentComparisonCheckConfig()
        return RequestedIDDocumentComparisonCheck(config)
