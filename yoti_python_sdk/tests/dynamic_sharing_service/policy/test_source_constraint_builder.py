from yoti_python_sdk.dynamic_sharing_service.policy.source_constraint_builder import (
    SourceConstraintBuilder,
)
from yoti_python_sdk.config import ANCHOR_VALUE_DRIVING_LICENCE, ANCHOR_VALUE_PASSPORT


def test_build():
    constraint = SourceConstraintBuilder().build()

    assert constraint["type"] == "SOURCE"
    assert not constraint["preferred_sources"]["soft_preference"]
    assert constraint["preferred_sources"]["anchors"] == []


def test_with_driving_licence():
    constraint = SourceConstraintBuilder().with_driving_licence().build()

    anchors = constraint["preferred_sources"]["anchors"]
    assert len(anchors) == 1
    assert ANCHOR_VALUE_DRIVING_LICENCE in [a["name"] for a in anchors]


def test_with_soft_preference():
    constraint = (
        SourceConstraintBuilder()
        .with_passport()
        .with_driving_licence()
        .with_soft_preference()
        .build()
    )
    anchors = constraint["preferred_sources"]["anchors"]
    assert len(anchors) == 2
    assert ANCHOR_VALUE_DRIVING_LICENCE in [a["name"] for a in anchors]
    assert ANCHOR_VALUE_PASSPORT in [a["name"] for a in anchors]
    assert constraint["preferred_sources"]["soft_preference"]


def test_with_is_strictly_latin_set_true():
    constraint = SourceConstraintBuilder().allow_strictly_latin().build()

    assert constraint["is_strictly_latin"] is True


def test_with_is_strictly_latin_set_false():
    constraint = SourceConstraintBuilder().disable_strictly_latin().build()

    assert constraint["is_strictly_latin"] is False


def test_with_is_strictly_latin_default():
    constraint = SourceConstraintBuilder().build()

    assert "is_strictly_latin" not in constraint
