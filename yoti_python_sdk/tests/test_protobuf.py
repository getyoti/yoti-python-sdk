# -*- coding: utf-8 -*-
import logging

import pytest

from yoti_python_sdk.protobuf import protobuf

string_value = "123"
byte_value = str.encode(string_value)
int_value = int(string_value)


@pytest.fixture(scope='module')
def proto():
    return protobuf.Protobuf()


@pytest.mark.parametrize(
    "content_type, expected_value",
    [(proto().CT_STRING, string_value),
     (proto().CT_DATE, string_value),
     (proto().CT_INT, int_value)])
def test_protobuf_values_based_on_content_type(content_type, expected_value):
    result = proto().value_based_on_content_type(byte_value, content_type)
    assert result == expected_value


def test_warning_protobuf_values_based_on_content_type(proto):
    # disable logging for the below types: warning shown as type is not recognized
    logger = logging.getLogger()
    logger.propagate = False

    result = proto.value_based_on_content_type(byte_value, proto.CT_UNDEFINED)
    assert result == string_value

    result = proto.value_based_on_content_type(byte_value)
    assert result == string_value

    result = proto.value_based_on_content_type(byte_value, 100)
    assert result == string_value

    logger.propagate = True


@pytest.mark.parametrize(
    "content_type",
    (proto().CT_JPEG,
     proto().CT_PNG))
def test_image_value_based_on_content_type(proto, content_type):
    result = proto.value_based_on_content_type(byte_value, content_type)
    assert result.data == byte_value
    assert result.content_type == content_type


def test_protobuf_image_uri_based_on_content_type(proto):
    value = b'test string'

    result = proto.image_uri_based_on_content_type(value, proto.CT_JPEG)
    assert result == 'data:image/jpeg;base64,dGVzdCBzdHJpbmc='

    result = proto.image_uri_based_on_content_type(value, proto.CT_PNG)
    assert result == 'data:image/png;base64,dGVzdCBzdHJpbmc='
