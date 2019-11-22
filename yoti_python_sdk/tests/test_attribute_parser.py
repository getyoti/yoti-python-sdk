# -*- coding: utf-8 -*-
import logging

import pytest

from datetime import date

from yoti_python_sdk import attribute_parser
from yoti_python_sdk.protobuf.protobuf import Protobuf

STRING_VALUE = "123"
BYTE_VALUE = str.encode(STRING_VALUE)
INT_VALUE = int(STRING_VALUE)

DATE_VALUE = "1995-04-20"
DATE_BYTE_VALUE = str.encode(DATE_VALUE)

INCORRECT_DATE_VALUE = "95-222-10"
INCORRECT_DATE_BYTE_VALUE = str.encode(INCORRECT_DATE_VALUE)


@pytest.fixture(scope="module")
def proto():
    return Protobuf()


@pytest.mark.parametrize(
    "content_type, expected_value",
    [(Protobuf.CT_STRING, STRING_VALUE), (Protobuf.CT_INT, INT_VALUE)],
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


def test_date_proto_should_parse_into_date_object():
    result = attribute_parser.value_based_on_content_type(
        DATE_BYTE_VALUE, Protobuf.CT_DATE
    )
    assert isinstance(result, date)
    assert result.strftime("%Y-%m-%d") == DATE_VALUE
    assert result.year == 1995
    assert result.month == 4
    assert result.day == 20


def test_should_raise_value_error_on_incorrect_format_date():
    with pytest.raises(ValueError):
        attribute_parser.value_based_on_content_type(
            INCORRECT_DATE_BYTE_VALUE, Protobuf.CT_DATE
        )
