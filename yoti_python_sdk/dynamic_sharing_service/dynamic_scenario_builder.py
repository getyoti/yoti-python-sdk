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

    def with_policy(self, policy):
        """
        :param policy: A DynamicPolicy defining the attributes to be requested
        """
        self.__scenario["policy"] = policy
        return self

    def with_extension(self, extension):
        """
        :param extension: An extension to be activated for the scenario
        """
        self.__scenario["extensions"].append(extension)
        return self

    def with_callback_endpoint(self, callback_endpoint):
        """
        :param callback_endpoint: A string with the callback endpoint
        """
        self.__scenario["callback_endpoint"] = callback_endpoint
        return self

    def build(self):
        """
        :returns: Dictionary representation of dynamic scenario
        """
        scenario = self.__scenario.copy()
        scenario["extensions"] = scenario["extensions"][:]
        return scenario
