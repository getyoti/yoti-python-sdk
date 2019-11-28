import pytest
import yoti_python_sdk.attribute

from yoti_python_sdk import config
from yoti_python_sdk.tests import anchor_fixture_parser

NAME = "name"
VALUE = "value"


def test_attribute_get_values():
    parsed_anchors = tuple()

    attribute = yoti_python_sdk.attribute.Attribute(NAME, VALUE, tuple())

    assert attribute.name == NAME
    assert attribute.value == VALUE
    assert attribute.anchors == parsed_anchors


def test_attribute_get_sources():
    anchors = create_source_and_verifier_anchors()
    attribute = yoti_python_sdk.attribute.Attribute(NAME, VALUE, anchors)
    sources = attribute.sources

    assert len(sources) == 1
    assert sources[0].anchor_type == config.ANCHOR_SOURCE


def test_attribute_get_verifiers():
    anchors = create_source_and_verifier_anchors()
    attribute = yoti_python_sdk.attribute.Attribute(NAME, VALUE, anchors)
    verifiers = attribute.verifiers

    assert len(verifiers) == 1
    assert verifiers[0].anchor_type == config.ANCHOR_VERIFIER


def create_source_and_verifier_anchors():
    passport_anchor = anchor_fixture_parser.get_parsed_passport_anchor()  # source
    yoti_admin_anchor = anchor_fixture_parser.get_parsed_yoti_admin_anchor()  # verifier

    return passport_anchor, yoti_admin_anchor


def test_attribute_name_is_immutable():
    attribute = yoti_python_sdk.attribute.Attribute(NAME, VALUE, tuple())

    with pytest.raises(AttributeError) as ex:
        attribute.name = "someOtherName"

    assert "can't set attribute" in str(ex.value)


def test_attribute_value_is_immutable():
    attribute = yoti_python_sdk.attribute.Attribute(NAME, VALUE, tuple())

    with pytest.raises(AttributeError) as ex:
        attribute.value = "someOtherValue"

    assert "can't set attribute" in str(ex.value)


def test_attribute_anchors_is_immutable():
    attribute = yoti_python_sdk.attribute.Attribute(NAME, VALUE, tuple())

    with pytest.raises(AttributeError) as ex:
        attribute.anchors = "someFirstAnchor", "someSecondAnchor"

    assert "can't set attribute" in str(ex.value)
