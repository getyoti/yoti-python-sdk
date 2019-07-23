# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
Builder for WantedAttribute
"""


class WantedAttributeBuilder(object):
    def __init__(self):
        self.__attribute = {}

    """
    @param name Sets name
    """

    def withName(self, name):
        self.__attribute["name"] = name
        return self

    """
    @param derivation Sets derivation
    """

    def withDerivation(self, derivation):
        self.__attribute["derivation"] = derivation
        return self

    """
    @return The wanted attribute object
    """

    def build(self):
        return self.__attribute.copy()
