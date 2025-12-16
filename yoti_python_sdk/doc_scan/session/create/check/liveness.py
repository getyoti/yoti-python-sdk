# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.doc_scan import constants
from yoti_python_sdk.utils import YotiSerializable, remove_null_values
from .requested_check import RequestedCheck


class RequestedLivenessCheckConfig(YotiSerializable):
    """
    The configuration applied when creating a Liveness Check
    """

    def __init__(self, liveness_type, max_retries, manual_check=None):
        """
        :param liveness_type: the liveness type
        :type liveness_type: str
        :param max_retries: the maximum number of retries
        :type max_retries: int
        :param manual_check: the manual check value
        :type manual_check: str or None
        """
        self.__liveness_type = liveness_type
        self.__max_retries = max_retries
        self.__manual_check = manual_check

    @property
    def liveness_type(self):
        """
        The type of the liveness check, e.g. "ZOOM"

        :return: the liveness type
        """
        return self.__liveness_type

    @property
    def max_retries(self):
        """
        The maximum number of retries a user is allowed for a liveness check

        :return: the maximum number of retries
        """
        return self.__max_retries

    @property
    def manual_check(self):
        """
        The manual check value for the liveness check

        :return: the manual check value
        :rtype: str or None
        """
        return self.__manual_check

    def to_json(self):
        return remove_null_values(
            {
                "liveness_type": self.liveness_type,
                "max_retries": self.max_retries,
                "manual_check": self.manual_check,
            }
        )


class RequestedLivenessCheck(RequestedCheck):
    """
    Requests creation of a Liveness Check
    """

    def __init__(self, liveness_check_config):
        """
        :param liveness_check_config: the requested liveness check configuration
        :type liveness_check_config: RequestedLivenessCheckConfig
        """
        self.__config = liveness_check_config

    @property
    def type(self):
        return constants.LIVENESS

    @property
    def config(self):
        return self.__config


class RequestedLivenessCheckBuilder(object):
    """
    Builder to assist creation of :class:`RequestedLivenessCheck`
    """

    def __init__(self):
        self.__liveness_type = None
        self.__max_retries = None
        self.__manual_check = None

    def for_zoom_liveness(self):
        """
        Sets the liveness type to "ZOOM"

        :return: the builder
        :rtype: RequestedLivenessCheckBuilder
        """
        return self.with_liveness_type(constants.ZOOM)

    def for_static_liveness(self):
        """
        Sets the liveness type to "STATIC"

        :return: the builder
        :rtype: RequestedLivenessCheckBuilder
        """
        return self.with_liveness_type(constants.STATIC)

    def with_liveness_type(self, liveness_type):
        """
        Sets the liveness type on the builder

        :param liveness_type: the liveness type
        :type liveness_type: str
        :return: the builder
        :rtype: RequestedLivenessCheckBuilder
        """
        self.__liveness_type = liveness_type
        return self

    def with_max_retries(self, max_retries):
        """
        Sets the maximum number of retries allowed for liveness check
        on the builder

        :param max_retries: the maximum number of retries
        :type max_retries: int
        :return: the builder
        :rtype: RequestedLivenessCheckBuilder
        """
        self.__max_retries = max_retries
        return self

    def with_manual_check_never(self):
        """
        Sets the manual check value to "NEVER"

        :return: the builder
        :rtype: RequestedLivenessCheckBuilder
        """
        self.__manual_check = constants.NEVER
        return self

    def build(self):
        config = RequestedLivenessCheckConfig(
            self.__liveness_type, self.__max_retries, self.__manual_check
        )
        return RequestedLivenessCheck(config)
