# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import iso8601
from iso8601 import ParseError


class MediaResponse(object):
    """
    Represents a media resource
    """

    def __init__(self, data=None):
        """
        :param data: the data to parse
        :type data: dict or None
        """
        if data is None:
            data = dict()

        self.__id = data.get("id", None)
        self.__type = data.get("type", None)
        self.__created = self.__parse_date(data.get("created", None))
        self.__last_updated = self.__parse_date(data.get("last_updated", None))

    @staticmethod
    def __parse_date(date):
        if date is None:
            return date

        try:
            return iso8601.parse_date(date)
        except ParseError:
            return None

    @property
    def id(self):
        """
        The ID of the media resource

        :return: the ID
        :rtype: str or None
        """
        return self.__id

    @property
    def type(self):
        """
        The type of the media resource, e.g. "JSON"

        :return: the type
        :rtype: str or None
        """
        return self.__type

    @property
    def created(self):
        """
        The date the media resource was created

        :return: the created date
        :rtype: datetime.datetime or None
        """
        return self.__created

    @property
    def last_updated(self):
        """
        The date the media resource was last updated

        :return: the last updated date
        :rtype: datetime.datetime or None
        """
        return self.__last_updated
