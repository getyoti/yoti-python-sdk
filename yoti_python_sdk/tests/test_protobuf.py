# -*- coding: utf-8 -*-
import pytest

from yoti_python_sdk.protobuf import protobuf


@pytest.fixture(scope='module')
def proto():
    return protobuf.Protobuf()


def test_protobuf_value_based_on_content_type(proto):
    string_value = "123"
    byte_value = str.encode(string_value)
    int_value = int(string_value)

    result = proto.value_based_on_content_type(byte_value, proto.CT_UNDEFINED)
    assert result == string_value

    result = proto.value_based_on_content_type(byte_value, proto.CT_STRING)
    assert result == string_value

    result = proto.value_based_on_content_type(byte_value, proto.CT_DATE)
    assert result == string_value

    result = proto.value_based_on_content_type(byte_value, proto.CT_JPEG)
    assert result == byte_value

    result = proto.value_based_on_content_type(byte_value, proto.CT_PNG)
    assert result == byte_value

    result = proto.value_based_on_content_type(byte_value, proto.CT_INT)
    assert result == int_value

    result = proto.value_based_on_content_type(byte_value)
    assert result == string_value


def test_protobuf_image_uri_based_on_content_type(proto):
    value = b'test string'

    result = proto.image_uri_based_on_content_type(value, proto.CT_JPEG)
    assert result == 'data:image/jpeg;base64,dGVzdCBzdHJpbmc='

    result = proto.image_uri_based_on_content_type(value, proto.CT_PNG)
    assert result == 'data:image/png;base64,dGVzdCBzdHJpbmc='
