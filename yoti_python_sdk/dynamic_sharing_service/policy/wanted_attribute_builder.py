# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .wanted_attribute import WantedAttribute

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
        self.__attribute["_WantedAttribute__name"] = name
        return self

    """
    @param derivation Sets derivation
    """

    def withDerivation(self, derivation):
        self.__attribute["_WantedAttribute__derivation"] = derivation
        return self

    """
    @return The wanted attribute object
    """

    def build(self):
        return WantedAttribute(**self.__attribute)
