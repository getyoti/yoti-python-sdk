# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class BreakdownResponse(object):
    """
    Represents one breakdown item for a given check
    """

    def __init__(self, data):
        """
        :param data: the data to parse
        :type data: dict
        """
        self.__sub_check = data.get("sub_check", None)
        self.__result = data.get("result", None)
        self.__details = [DetailsResponse(detail) for detail in data.get("details", [])]

    @property
    def sub_check(self):
        """
        The sub check value for the breakdown

        :return: the sub check value
        :rtype: str or None
        """
        return self.__sub_check

    @property
    def result(self):
        """
        The result of the sub check

        :return: the result
        :rtype: str or None
        """
        return self.__result

    @property
    def details(self):
        """
        The details of the sub check

        :return: the details
        :rtype: list[DetailsResponse]
        """
        return self.__details


class DetailsResponse(object):
    """
    Represents a specific detail for a breakdown
    """

    def __init__(self, data):
        self.__name = data.get("name", None)
        self.__value = data.get("value", None)

    @property
    def name(self):
        """
        The name of the details item

        :return: the name
        :rtype: str or None
        """
        return self.__name

    @property
    def value(self):
        """
        The value of the details item

        :return: the value
        :rtype: str or None
        """
        return self.__value
