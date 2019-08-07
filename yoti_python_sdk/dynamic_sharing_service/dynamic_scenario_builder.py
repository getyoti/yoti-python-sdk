# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .policy.dynamic_policy_builder import DynamicPolicyBuilder


class DynamicScenarioBuilder(object):
    def __init__(self):
        self.__scenario = {
            "policy": DynamicPolicyBuilder().build(),
            "extensions": [],
            "callback_endpoint": "",
        }

    """
    @param policy A DynamicPolicy defining the attributes to be shared
    """

    def with_policy(self, policy):
        self.__scenario["policy"] = policy
        return self

    """
    @param extension An extension to be activated for the scenario
    """

    def with_extension(self, extension):
        self.__scenario["extensions"].append(extension)
        return self

    """
    @param callback_endpoint A string with the callback endpoint
    """

    def with_callback_endpoint(self, callback_endpoint):
        self.__scenario["callback_endpoint"] = callback_endpoint
        return self

    """
    @return Dictionary representation of dynamic scenario
    """

    def build(self):
        return self.__scenario.copy()
