# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.doc_scan import constants
from yoti_python_sdk.utils import YotiSerializable, remove_null_values
from .requested_task import RequestedTask


class RequestedTextExtractionTaskConfig(YotiSerializable):
    def __init__(self, manual_check, chip_data=None):
        """
        :param manual_check: the manual check value
        :type manual_check: str
        """
        self.__manual_check = manual_check
        self.__chip_data = chip_data

    @property
    def manual_check(self):
        """
        Describes the manual fallback behaviour applied to each Task

        :return: the manual check value
        """
        return self.__manual_check

    @property
    def chip_data(self):
        """
        Describes how to use chip data from an ID document if
        it is available

        :return: the chip data usage
        """
        return self.__chip_data

    def to_json(self):
        return remove_null_values(
            {"manual_check": self.manual_check, "chip_data": self.chip_data}
        )


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
        self.__chip_data = None

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

    def with_chip_data_desired(self):
        """
        The TextExtractionTask will use chip data if it is available

        :return: the builder
        :rtype: RequestedTextExtractionTaskBuilder
        """
        self.__chip_data = constants.DESIRED
        return self

    def with_chip_data_ignore(self):
        """
        The TextExtractionTask will ignore chip data

        :return: the builder
        :rtype: RequestedTextExtractionTaskBuilder
        """
        self.__chip_data = constants.IGNORE
        return self

    def build(self):
        config = RequestedTextExtractionTaskConfig(
            self.__manual_check, self.__chip_data
        )
        return RequestedTextExtractionTask(config)
