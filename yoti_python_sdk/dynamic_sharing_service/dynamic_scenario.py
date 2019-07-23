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

    """
    @return A list of Extensions
    """

    @property
    def extensions(self):
        return self.__extensions

    """
    @return A string containing the callback endpoint
    """

    @property
    def callback_endpoint(self):
        return self.__callback_endpoint

    """
    @return A nested dictionary with key-values that match the api
    """

    @property
    def data(self):
        return {
            "callback_endpoint": self.callback_endpoint,
            "policy": self.policy.data,
            "extensions": [extension.data for extension in self.extensions],
        }
