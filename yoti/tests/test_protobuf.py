import base64
import pytest

from yoti.protobuf.v1 import protobuf


@pytest.fixture(scope='module')
def proto():
    return protobuf.Protobuf()


def test_protobuf_value_based_on_content_type(proto):
    value = b'test string'

    with pytest.raises(TypeError):
        proto.value_based_on_content_type(value, proto.CT_UNDEFINED)

    result = proto.value_based_on_content_type(value, proto.CT_STRING)
    assert isinstance(result, str)

    result = proto.value_based_on_content_type(value, proto.CT_JPEG)
    assert result == 'data:image/jpeg;base64,dGVzdCBzdHJpbmc='

    result = proto.value_based_on_content_type(value, proto.CT_DATE)
    assert isinstance(result, str)

    result = proto.value_based_on_content_type(value, proto.CT_PNG)
    assert result == 'data:image/png;base64,dGVzdCBzdHJpbmc='

    result = proto.value_based_on_content_type(value)
    assert result == value


# def test_protobuf_current_user(proto):
#     with pytest.raises(ValueError):
#         proto.current_user({})
#
#     value = 'test text'
#     encoded_value = base64.b64encode(value.encode('utf-8'))
#     receipt = {'other_party_profile_content': encoded_value}
#     current_user = proto.current_user(receipt)
#     assert isinstance(current_user, compubapi.EncryptedData)
