# -*- coding: utf-8 -*-
from yoti_python_sdk.image import Image


def assert_is_expected_image(image, image_type, expected_base64_last10):
    assert isinstance(image, Image)
    assert image.content_type == image_type
    assert image.mime_type() == "image/" + image_type
    assert image.base64_content()[-10:] == expected_base64_last10
