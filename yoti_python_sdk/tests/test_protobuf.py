# -*- coding: utf-8 -*-
import pytest
from past.builtins import basestring

from protobuf import protobuf


@pytest.fixture(scope='module')
def proto():
    return protobuf.Protobuf()


def test_protobuf_value_based_on_content_type(proto):
    value = b'test string'

    with pytest.raises(TypeError):
        proto.value_based_on_content_type(value, proto.CT_UNDEFINED)

    result = proto.value_based_on_content_type(value, proto.CT_STRING)
    assert isinstance(result, basestring)

    result = proto.value_based_on_content_type(value, proto.CT_DATE)
    assert isinstance(result, basestring)

    result = proto.value_based_on_content_type(value)
    assert result == value


def test_protobuf_image_uri_based_on_content_type(proto):
    value = b'test string'

    result = proto.image_uri_based_on_content_type(value, proto.CT_JPEG)
    assert result == 'data:image/jpeg;base64,dGVzdCBzdHJpbmc='

    result = proto.image_uri_based_on_content_type(value, proto.CT_PNG)
    assert result == 'data:image/png;base64,dGVzdCBzdHJpbmc='
