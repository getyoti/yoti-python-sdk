# -*- coding: utf-8 -*-
import pytest

from yoti_python_sdk.image import Image
from yoti_python_sdk.protobuf.protobuf import Protobuf


def test_image_with_unsupported_type():
    with pytest.raises(TypeError):
        Image(b"", Protobuf.CT_UNDEFINED)


@pytest.mark.parametrize(
    "content_type, expected_mime_type",
    [(Protobuf.CT_JPEG, "image/jpeg"), (Protobuf.CT_PNG, "image/png")],
)
def test_image_mime_type(content_type, expected_mime_type):
    image = Image(b"", content_type)

    assert image.mime_type() == expected_mime_type


@pytest.mark.parametrize(
    "content_type, expected_base64_content",
    [
        (Protobuf.CT_JPEG, "data:image/jpeg;base64,dGVzdCBzdHJpbmc="),
        (Protobuf.CT_PNG, "data:image/png;base64,dGVzdCBzdHJpbmc="),
    ],
)
def test_image_base64_content(content_type, expected_base64_content):
    image = Image(b"test string", content_type)
    assert image.base64_content() == expected_base64_content
