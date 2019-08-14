# -*- coding: utf-8 -*-
import logging

import pytest

from yoti_python_sdk import attribute_parser
from yoti_python_sdk.protobuf import protobuf

STRING_VALUE = "123"
BYTE_VALUE = str.encode(STRING_VALUE)
INT_VALUE = int(STRING_VALUE)


@pytest.fixture(scope="module")
def proto():
    return protobuf.Protobuf()


@pytest.mark.parametrize(
    "content_type, expected_value",
    [
        (protobuf.Protobuf.CT_STRING, STRING_VALUE),
        (protobuf.Protobuf.CT_DATE, STRING_VALUE),
        (protobuf.Protobuf.CT_INT, INT_VALUE),
    ],
)
def test_attribute_parser_values_based_on_content_type(content_type, expected_value):
    result = attribute_parser.value_based_on_content_type(BYTE_VALUE, content_type)
    assert result == expected_value


def test_attribute_parser_values_based_on_other_content_types(proto):
    # disable logging for the below types: warning shown as type is not recognized
    logger = logging.getLogger()
    logger.propagate = False

    result = attribute_parser.value_based_on_content_type(
        BYTE_VALUE, proto.CT_UNDEFINED
    )
    assert result == STRING_VALUE

    result = attribute_parser.value_based_on_content_type(BYTE_VALUE)
    assert result == STRING_VALUE

    result = attribute_parser.value_based_on_content_type(BYTE_VALUE, 100)
    assert result == STRING_VALUE

    logger.propagate = True


def test_png_image_value_based_on_content_type(proto):
    result = attribute_parser.value_based_on_content_type(BYTE_VALUE, proto.CT_PNG)
    assert result.data == BYTE_VALUE
    assert result.content_type == "png"


def test_jpeg_image_value_based_on_content_type(proto):
    result = attribute_parser.value_based_on_content_type(BYTE_VALUE, proto.CT_JPEG)
    assert result.data == BYTE_VALUE
    assert result.content_type == "jpeg"
