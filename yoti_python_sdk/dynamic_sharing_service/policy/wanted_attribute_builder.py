# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
Builder for WantedAttribute
"""


class WantedAttributeBuilder(object):
    def __init__(self):
        self.__attribute = {}

    def with_name(self, name):
        """
        :param name: Sets name
        """
        self.__attribute["name"] = name
        return self

    def with_derivation(self, derivation):
        """
        :param derivation: Sets derivation
        """
        self.__attribute["derivation"] = derivation
        return self

    def build(self):
        """
        :return: The wanted attribute object
        """
        return self.__attribute.copy()
