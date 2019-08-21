from yoti_python_sdk.dynamic_sharing_service.policy.wanted_anchor_builder import (
    WantedAnchorBuilder,
)


def test_build():
    TEST_VALUE = "TEST VALUE"
    TEST_SUB_TYPE = "TEST SUB TYPE"

    builder = WantedAnchorBuilder()
    builder.with_value(TEST_VALUE)
    builder.with_subtype(TEST_SUB_TYPE)

    anchor = builder.build()

    assert anchor["name"] == TEST_VALUE
    assert anchor["sub_type"] == TEST_SUB_TYPE
