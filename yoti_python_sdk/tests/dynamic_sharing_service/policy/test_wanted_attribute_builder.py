from yoti_python_sdk.dynamic_sharing_service.policy.wanted_attribute_builder import (
    WantedAttributeBuilder,
)
from yoti_python_sdk.dynamic_sharing_service.policy.source_constraint_builder import (
    SourceConstraintBuilder,
)

import pytest


def test_build():
    NAME = "Test name"
    DERIVATION = "Test derivation"

    builder = WantedAttributeBuilder()

    attribute = builder.with_name(NAME).with_derivation(DERIVATION).build()

    assert attribute["name"] == NAME
    assert attribute["derivation"] == DERIVATION


def test_with_constraint():
    constraint = SourceConstraintBuilder().with_driving_licence().build()
    attribute = (
        WantedAttributeBuilder()
        .with_name("test name")
        .with_constraint(constraint)
        .build()
    )

    constraints = attribute["constraints"]
    assert len(constraints) == 1
    assert len(constraints[0]["preferred_sources"]["anchors"]) == 1


def test_with_multiple_constraints():
    constraintA = SourceConstraintBuilder().with_driving_licence().build()
    constraintB = SourceConstraintBuilder().with_passport().build()

    attribute = (
        WantedAttributeBuilder()
        .with_name("test name")
        .with_constraint([constraintA, constraintB])
        .build()
    )

    constraints = attribute["constraints"]
    assert len(constraints) == 2


def test_missing_attribute_name_raises():
    with pytest.raises(ValueError):
        WantedAttributeBuilder().build()


def test_acccept_self_assert():
    attribute = (
        WantedAttributeBuilder()
        .with_name("test name")
        .with_accept_self_asserted()
        .build()
    )
    assert attribute["accept_self_asserted"]
