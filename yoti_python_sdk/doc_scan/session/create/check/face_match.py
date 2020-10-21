# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.doc_scan import constants
from yoti_python_sdk.utils import YotiSerializable, remove_null_values
from .requested_check import RequestedCheck


class RequestedFaceMatchCheckConfig(YotiSerializable):
    """
    The configuration applied when creating a FaceMatch Check
    """

    def __init__(self, manual_check):
        """
        :param manual_check: the manual check value
        :type manual_check: str
        """
        self.__manual_check = manual_check

    @property
    def manual_check(self):
        """
        Returns a value for a manual check for a given
        FaceMatch Check

        :return: the manual check value
        :rtype: str
        """
        return self.__manual_check

    def to_json(self):
        return remove_null_values({"manual_check": self.manual_check})


class RequestedFaceMatchCheck(RequestedCheck):
    """
    Requests creation of a FaceMatch Check
    """

    def __init__(self, config):
        """
        :param config: the requested FaceMatch check configuration
        :type config: RequestedFaceMatchCheckConfig
        """
        self.__config = config

    @property
    def type(self):
        return constants.ID_DOCUMENT_FACE_MATCH

    @property
    def config(self):
        return self.__config


class RequestedFaceMatchCheckBuilder(object):
    """
    Builder to assist with creation of :class:`RequestedFaceMatchCheck`
    """

    def __init__(self):
        self.__manual_check = None

    def with_manual_check_always(self):
        """
        Sets the value of manual check to "ALWAYS"

        :return: the builder
        :rtype: RequestedFaceMatchCheckBuilder
        """
        self.__manual_check = constants.ALWAYS
        return self

    def with_manual_check_fallback(self):
        """
        Sets the value of manual check to "FALLBACK"

        :return: the builder
        :rtype: RequestedFaceMatchCheckBuilder
        """
        self.__manual_check = constants.FALLBACK
        return self

    def with_manual_check_never(self):
        """
        Sets the value of manual check to "NEVER"

        :return: the builder
        :rtype: RequestedFaceMatchCheckBuilder
        """
        self.__manual_check = constants.NEVER
        return self

    def build(self):
        config = RequestedFaceMatchCheckConfig(self.__manual_check)
        return RequestedFaceMatchCheck(config)
