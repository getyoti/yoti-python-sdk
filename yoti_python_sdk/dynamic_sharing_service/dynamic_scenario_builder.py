# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .dynamic_scenario import DynamicScenario
from .policy.dynamic_policy_builder import DynamicPolicyBuilder


class DynamicScenarioBuilder(object):
    def __init__(self):
        self.__scenario = {
            "_DynamicScenario__policy": DynamicPolicyBuilder().build(),
            "_DynamicScenario__extensions": [],
            "_DynamicScenario__callback_endpoint": "",
        }

    """
    @param policy A DynamicPolicy defining the attributes to be shared
    """

    def with_policy(self, policy):
        self.__scenario["_DynamicScenario__policy"] = policy
        return self

    """
    @param extension A Extensions to add to the scenario
    """

    def with_extension(self, extension):
        self.__scenario["_DynamicScenario__extensions"].append(extension)
        return self

    """
    @param callback_endpoint A string with the callback endpoint
    """

    def with_callback_endpoint(self, callback_endpoint):
        self.__scenario["_DynamicScenario__callback_endpoint"] = callback_endpoint
        return self

    """
    @return A DynamicScenario
    """

    def build(self):
        return DynamicScenario(**self.__scenario)
