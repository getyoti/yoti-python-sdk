import yoti_python_sdk.attribute


def test_attribute_get_values():
    name = "name"
    value = "value"
    parsed_anchors = []

    attribute = yoti_python_sdk.attribute.attribute(name, value, parsed_anchors)

    assert attribute.get_name() == name
    assert attribute.get_value() == value
    assert attribute.get_anchors() == parsed_anchors
