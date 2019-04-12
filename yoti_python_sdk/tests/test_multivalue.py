# -*- coding: utf-8 -*-
from yoti_python_sdk import multivalue
from yoti_python_sdk.image import Image
from yoti_python_sdk.tests import attribute_fixture_parser, image_helper


def test_multi_value_filter_image():
    multi_value = attribute_fixture_parser.parse_multi_value()
    multi_value.append(0)
    multi_value.append("string_value")

    assert len(multi_value) == 4

    filtered_list = multivalue.filter_values(multi_value, Image)

    assert len(filtered_list) == 2

    image_helper.assert_is_expected_image(filtered_list[0], "jpeg", "vWgD//2Q==")
    image_helper.assert_is_expected_image(filtered_list[1], "jpeg", "38TVEH/9k=")


def test_multi_value_filter_int():
    int_value = 0
    multi_value = [int_value, "string_value"]

    assert len(multi_value) == 2

    filtered_list = multivalue.filter_values(multi_value, int)

    assert len(filtered_list) == 1
    assert filtered_list[0] is int_value


def test_multi_value_filter_string():
    string_value = "string_value"
    multi_value = [0, string_value]

    assert len(multi_value) == 2

    filtered_list = multivalue.filter_values(multi_value, str)

    assert len(filtered_list) == 1
    assert filtered_list[0] is string_value


def test_multi_value_filter_is_immutable():
    original_string_value = "string_value"
    multi_value = [0, original_string_value]

    filtered_list = multivalue.filter_values(multi_value, str)

    filtered_list[0] == "changed_string_value"

    assert filtered_list[0] == original_string_value
