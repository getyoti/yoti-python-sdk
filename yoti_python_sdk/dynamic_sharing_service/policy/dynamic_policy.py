# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
Defines a list of wanted attributes
"""


class DynamicPolicy(object):
    SELFIE_AUTH_TYPE = 1
    PIN_AUTH_TYPE = 2

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    """
    @return List of attributes to be requested
    """

    @property
    def wanted_attributes(self):
        return self.__wanted_attributes

    """
    @return Represents the authentication types to be used
    """

    @property
    def wanted_auth_types(self):
        return self.__wanted_auth_types

    @property
    def is_wanted_remember_me(self):
        return self.__is_wanted_remember_me
