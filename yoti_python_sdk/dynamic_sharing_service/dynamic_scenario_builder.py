# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .dynamic_scenario import DynamicScenario
from .policy.dynamic_policy_builder import DynamicPolicyBuilder


class DynamicScenarioBuilder(object):
    def __init__(self):
        self.__scenario = {"_DynamicScenario__policy": DynamicPolicyBuilder().build()}

    """
    @param policy A DynamicPolicy defining the attributes to be shared
    """

    def with_policy(self, policy):
        self.__scenario["_DynamicScenario__policy"] = policy
        return self

    """
    @return A DynamicScenario
    """

    def build(self):
        return DynamicScenario(**self.__scenario)
