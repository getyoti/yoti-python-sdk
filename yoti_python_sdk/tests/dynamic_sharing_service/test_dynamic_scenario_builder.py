# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.dynamic_sharing_service.dynamic_scenario_builder import (
    DynamicScenarioBuilder,
)
from yoti_python_sdk.dynamic_sharing_service.policy.dynamic_policy_builder import (
    DynamicPolicyBuilder,
)


def test_build_scenario():
    EXTENSION1 = "Extension 1"
    EXTENSION2 = "Extension 2"
    CALLBACK_ENDPOINT = "Callback Endpoint"

    scenario = (
        DynamicScenarioBuilder()
        .with_policy(
            DynamicPolicyBuilder().with_full_name().with_wanted_remember_me().build()
        )
        .with_extension(EXTENSION1)
        .with_extension(EXTENSION2)
        .with_callback_endpoint(CALLBACK_ENDPOINT)
        .build()
    )

    assert len(scenario["policy"]["wanted"]) == 1
    assert scenario["policy"]["wanted_remember_me"]
    assert len(scenario["extensions"]) == 2
    assert EXTENSION1 in scenario["extensions"]
    assert EXTENSION2 in scenario["extensions"]
    assert scenario["callback_endpoint"] == CALLBACK_ENDPOINT
