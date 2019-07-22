# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class DynamicScenario(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    """
    @return A DynamicPolicy defining the attributes to be shared
    """

    @property
    def policy(self):
        return self.__policy
