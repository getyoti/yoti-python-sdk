from yoti_python_sdk.dynamic_sharing_service.policy.wanted_attribute_builder import (
    WantedAttributeBuilder,
)


def test_build():
    NAME = "Test name"
    DERIVATION = "Test derivation"

    builder = WantedAttributeBuilder()

    attribute = builder.withName(NAME).withDerivation(DERIVATION).build()

    assert attribute["name"] == NAME
    assert attribute["derivation"] == DERIVATION
