# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.doc_scan import constants
from yoti_python_sdk.utils import YotiSerializable, remove_null_values
from .requested_check import RequestedCheck


class WatchlistScreeningCheckConfig(YotiSerializable):
    """
    The configuration applied when creating a Watchlist screening check.
    """

    def __init__(self, manual_check, categories):
        """
        :param manual_check: the watchlist screening check manual_check eg. "NEVER"
        :type type: str
        :param categories: list of categories for watchlist screening check config
        :type max_retries: list
        """
        self.__categories = categories
        self.__manual_check = manual_check

    @property
    def manual_check(self):
        """
        Watchlist screening check manual check value

        :return: str
        """
        return self.__manual_check

    @property
    def categories(self):
        """
        Watchlist screening check categories

        :return: list
        """
        return self.__categories

    def to_json(self):
        return remove_null_values(
            {"manual_check": self.manual_check, "categories": self.__categories}
        )


class WatchlistScreeningCheck(RequestedCheck):
    """
    Requests creation of a Watchlist screening check
    """

    def __init__(self, config):
        """
        :param config: the Watchlist screening check configuration
        :type config: WatchlistScreeningCheckConfig
        """
        self.__config = config

    @property
    def type(self):
        return constants.WATCHLIST_SCREENING_CHECK_TYPE

    @property
    def config(self):
        return self.__config


class WatchlistScreeningCheckBuilder(object):
    """
    Builder to assist creation of :class:`WatchlistScreeningCheck`
    """

    def __init__(self):
        self.__categories = None
        self.__manual_check = None

    def with_categories(self, categories):
        """
        Sets the WatchListScreeningCheck categories

        :return: the builder
        :rtype: WatchlistScreeningCheckBuilder
        """
        self.__categories = categories

        return self

    def with_manual_check(self, manual_check):
        """
        Sets the WatchListScreeningCheck manual_check

        :param liveness_type: the manual_check
        :type liveness_type: str
        :return: the builder
        :rtype: WatchlistScreeningCheckBuilder
        """
        self.__manual_check = manual_check

        return self

    def build(self):
        config = WatchlistScreeningCheckConfig(self.__manual_check, self.__categories or [])
        return WatchlistScreeningCheck(config)
