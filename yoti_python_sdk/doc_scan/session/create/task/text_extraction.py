# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.doc_scan import constants
from yoti_python_sdk.utils import YotiSerializable
from .requested_task import RequestedTask


class RequestedTextExtractionTaskConfig(YotiSerializable):
    def __init__(self, manual_check):
        """
        :param manual_check: the manual check value
        :type manual_check: str
        """
        self.__manual_check = manual_check

    @property
    def manual_check(self):
        """
        Describes the manual fallback behaviour applied to each Task

        :return: the manual check value
        """
        return self.__manual_check

    def to_json(self):
        return {"manual_check": self.manual_check}


class RequestedTextExtractionTask(RequestedTask):
    """
    Builder to assist creation of :class:`RequestedTextExtractionTask`
    """

    def __init__(self, config):
        """
        :param config: the text extraction task configuration
        :type config: RequestedTextExtractionTaskConfig
        """
        self.__config = config

    @property
    def type(self):
        return constants.ID_DOCUMENT_TEXT_DATA_EXTRACTION

    @property
    def config(self):
        return self.__config


class RequestedTextExtractionTaskBuilder(object):
    """
    Builder to assist creation of :class:`RequestedTextExtractionTask`
    """

    def __init__(self):
        self.__manual_check = None

    def with_manual_check_always(self):
        """
        Sets the manual check value to be "ALWAYS"

        :return: the builder
        :rtype: RequestedTextExtractionTaskBuilder
        """
        self.__manual_check = constants.ALWAYS
        return self

    def with_manual_check_fallback(self):
        """
        Sets the manual check value to be "FALLBACK"

        :return: the builder
        :rtype: RequestedTextExtractionTaskBuilder
        """
        self.__manual_check = constants.FALLBACK
        return self

    def with_manual_check_never(self):
        """
        Sets the manual check value to be "NEVER"

        :return: the builder
        :rtype: RequestedTextExtractionTaskBuilder
        """
        self.__manual_check = constants.NEVER
        return self

    def build(self):
        config = RequestedTextExtractionTaskConfig(self.__manual_check)
        return RequestedTextExtractionTask(config)
