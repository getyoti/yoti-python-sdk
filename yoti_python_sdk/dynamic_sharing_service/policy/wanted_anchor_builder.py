# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class WantedAnchorBuilder(object):
    def __init__(self):
        self.__name = ""
        self.__subtype = ""

    def with_value(self, name):
        """
        :param name: The type of anchor as a string
        """
        self.__name = name
        return self

    def with_subtype(self, subtype):
        """
        :param subtype: Subtype information as a string
        """
        self.__subtype = subtype
        return self

    def build(self):
        """
        :returns: A dict containing the anchor specification
        """
        return {"name": self.__name, "sub_type": self.__subtype}
