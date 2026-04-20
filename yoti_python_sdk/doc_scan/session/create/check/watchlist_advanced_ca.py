# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.doc_scan import constants
from yoti_python_sdk.utils import YotiSerializable, remove_null_values
from .requested_check import RequestedCheck


class WatchlistAdvancedCaProfilesCheckConfig(YotiSerializable):
    """
    The configuration applied when creating a Watchlist Advanced CA Profiles check.
    """

    def __init__(self, remove_deceased=None, share_url=None, sources=None):
        """
        :param remove_deceased: whether to remove deceased individuals from results
        :type remove_deceased: bool or None
        :param share_url: whether to share the URL in results
        :type share_url: bool or None
        :param sources: the sources configuration
        :type sources: WatchlistAdvancedCaSourcesConfig or None
        """
        self.__remove_deceased = remove_deceased
        self.__share_url = share_url
        self.__sources = sources

    @property
    def remove_deceased(self):
        """
        Whether deceased individuals are removed from results

        :return: remove deceased flag
        :rtype: bool or None
        """
        return self.__remove_deceased

    @property
    def share_url(self):
        """
        Whether the URL is shared in results

        :return: share URL flag
        :rtype: bool or None
        """
        return self.__share_url

    @property
    def sources(self):
        """
        The sources configuration for the advanced CA profiles check

        :return: the sources configuration
        :rtype: WatchlistAdvancedCaSourcesConfig or None
        """
        return self.__sources

    def to_json(self):
        return remove_null_values(
            {
                "remove_deceased": self.__remove_deceased,
                "share_url": self.__share_url,
                "sources": self.__sources,
            }
        )


class WatchlistAdvancedCaSourcesConfig(YotiSerializable):
    """
    Configures the sources for a Watchlist Advanced CA Profiles check.
    """

    def __init__(self, types=None):
        """
        :param types: the list of source types to check against
        :type types: list[str] or None
        """
        self.__types = types or []

    @property
    def types(self):
        """
        The list of source types

        :return: the source types
        :rtype: list[str]
        """
        return self.__types

    def to_json(self):
        return remove_null_values({"types": self.__types})


class WatchlistAdvancedCaProfilesCheck(RequestedCheck):
    """
    Requests creation of a Watchlist Advanced CA Profiles check
    """

    def __init__(self, config):
        """
        :param config: the Watchlist Advanced CA Profiles check configuration
        :type config: WatchlistAdvancedCaProfilesCheckConfig
        """
        self.__config = config

    @property
    def type(self):
        return constants.WATCHLIST_ADVANCED_CA_CHECK_TYPE

    @property
    def config(self):
        return self.__config


class WatchlistAdvancedCaProfilesCheckBuilder(object):
    """
    Builder to assist creation of :class:`WatchlistAdvancedCaProfilesCheck`
    """

    def __init__(self):
        self.__remove_deceased = None
        self.__share_url = None
        self.__sources = None

    def with_remove_deceased(self, remove_deceased):
        """
        Sets whether deceased individuals should be removed from results

        :param remove_deceased: the remove deceased flag
        :type remove_deceased: bool
        :return: the builder
        :rtype: WatchlistAdvancedCaProfilesCheckBuilder
        """
        self.__remove_deceased = remove_deceased
        return self

    def with_share_url(self, share_url):
        """
        Sets whether the URL should be shared in results

        :param share_url: the share URL flag
        :type share_url: bool
        :return: the builder
        :rtype: WatchlistAdvancedCaProfilesCheckBuilder
        """
        self.__share_url = share_url
        return self

    def with_sources(self, sources):
        """
        Sets the sources configuration for the check

        :param sources: the sources configuration
        :type sources: WatchlistAdvancedCaSourcesConfig
        :return: the builder
        :rtype: WatchlistAdvancedCaProfilesCheckBuilder
        """
        self.__sources = sources
        return self

    def build(self):
        config = WatchlistAdvancedCaProfilesCheckConfig(
            self.__remove_deceased, self.__share_url, self.__sources
        )
        return WatchlistAdvancedCaProfilesCheck(config)
