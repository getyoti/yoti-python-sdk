# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.dynamic_sharing_service.dynamic_scenario_builder import (
    DynamicScenarioBuilder,
)
from yoti_python_sdk.dynamic_sharing_service.policy.dynamic_policy_builder import (
    DynamicPolicyBuilder,
)
from yoti_python_sdk.dynamic_sharing_service.extension.extension_builder import (
    ExtensionBuilder,
)

from yoti_python_sdk import config


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

    assert len(scenario.policy.wanted_attributes) == 1
    assert scenario.policy.is_wanted_remember_me
    assert len(scenario.extensions) == 2
    assert EXTENSION1 in scenario.extensions
    assert EXTENSION2 in scenario.extensions
    assert scenario.callback_endpoint == CALLBACK_ENDPOINT


def test_serialization():
    CALLBACK_ENDPOINT = "Callback Endpoint"
    TEST_EXTENSION = "TEST_EXTENSION"

    extension = (
        ExtensionBuilder()
        .with_extension_type(TEST_EXTENSION)
        .with_content(None)
        .build()
    )
    policy = DynamicPolicyBuilder().with_age_over(18).build()

    data = (
        DynamicScenarioBuilder()
        .with_policy(policy)
        .with_extension(extension)
        .with_callback_endpoint(CALLBACK_ENDPOINT)
        .build()
        .data
    )

    assert data["callback_endpoint"] == CALLBACK_ENDPOINT
    assert len(data["policy"]["wanted"]) == 1
    assert config.ATTRIBUTE_AGE_OVER + "18" in [
        attr["derivation"] for attr in data["policy"]["wanted"]
    ]
    assert len(data["extensions"]) == 1
    assert TEST_EXTENSION in [extension["type"] for extension in data["extensions"]]
