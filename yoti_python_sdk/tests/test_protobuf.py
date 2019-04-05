# -*- coding: utf-8 -*-
import logging

import pytest

from yoti_python_sdk.protobuf import protobuf

STRING_VALUE = "123"
BYTE_VALUE = str.encode(STRING_VALUE)
INT_VALUE = int(STRING_VALUE)


@pytest.fixture(scope='module')
def proto():
    return protobuf.Protobuf()


@pytest.mark.parametrize(
    "content_type, expected_value",
    [(proto().CT_STRING, STRING_VALUE),
     (proto().CT_DATE, STRING_VALUE),
     (proto().CT_INT, INT_VALUE)])
def test_protobuf_values_based_on_content_type(content_type, expected_value):
    result = proto().value_based_on_content_type(BYTE_VALUE, content_type)
    assert result == expected_value


def test_protobuf_values_based_on_other_content_types(proto):
    # disable logging for the below types: warning shown as type is not recognized
    logger = logging.getLogger()
    logger.propagate = False

    result = proto.value_based_on_content_type(BYTE_VALUE, proto.CT_UNDEFINED)
    assert result == STRING_VALUE

    result = proto.value_based_on_content_type(BYTE_VALUE)
    assert result == STRING_VALUE

    result = proto.value_based_on_content_type(BYTE_VALUE, 100)
    assert result == STRING_VALUE

    logger.propagate = True


@pytest.mark.parametrize(
    "content_type",
    (proto().CT_JPEG,
     proto().CT_PNG))
def test_image_value_based_on_content_type(proto, content_type):
    result = proto.value_based_on_content_type(BYTE_VALUE, content_type)
    assert result.data == BYTE_VALUE
    assert result.content_type == content_type


def test_protobuf_image_uri_based_on_content_type(proto):
    value = b'test string'

    result = proto.image_uri_based_on_content_type(value, proto.CT_JPEG)
    assert result == 'data:image/jpeg;base64,dGVzdCBzdHJpbmc='

    result = proto.image_uri_based_on_content_type(value, proto.CT_PNG)
    assert result == 'data:image/png;base64,dGVzdCBzdHJpbmc='
