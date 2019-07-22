# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
Defines the wanted attribute and derivation
"""


class WantedAttribute(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    """
    @return Name identifying the attribute
    """

    @property
    def name(self):
        return self.__dict__.get("_WantedAttribute__name", None)

    """
    @return Additional derived criteria
    """

    @property
    def derivation(self):
        return self.__dict__.get("_WantedAttribute__derivation", None)
