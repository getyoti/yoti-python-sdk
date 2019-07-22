# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.dynamic_sharing_service.dynamic_scenario_builder import (
    DynamicScenarioBuilder,
)
from yoti_python_sdk.dynamic_sharing_service.policy.dynamic_policy_builder import (
    DynamicPolicyBuilder,
)


def test_build_scenario():
    scenario = (
        DynamicScenarioBuilder()
        .with_policy(
            DynamicPolicyBuilder().with_full_name().with_wanted_remember_me().build()
        )
        .build()
    )

    assert len(scenario.policy.wanted_attributes) == 1
    assert scenario.policy.is_wanted_remember_me
