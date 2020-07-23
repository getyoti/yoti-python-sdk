# -*- coding: utf-8 -*-
import pytest
import base64

from yoti_python_sdk.utils import urlsafe_b64encode_unpadded, urlsafe_b64decode_unpadded


@pytest.mark.parametrize(
    "b64url, b64",
    [
        ("HT-sGfUaHj-rDA", "HT+sGfUaHj+rDA=="),
        ("X_uuRoHwt9_B6g", "X/uuRoHwt9/B6g=="),
        ("eZU8xcW_eJ4", "eZU8xcW/eJ4="),
        ("-OyhuDs6dAg", "+OyhuDs6dAg="),
        ("c3RyaW5n", "c3RyaW5n"),
    ],
)
def test_urlsafe_b64decode_unpadded(b64url, b64):
    b64url_decoded = urlsafe_b64decode_unpadded(b64url)

    assert base64.b64encode(b64url_decoded).decode("UTF-8") == b64


@pytest.mark.parametrize(
    "b64url_padded, b64",
    [("HT-sGfUaHj-rDA==", "HT+sGfUaHj+rDA=="), ("eZU8xcW_eJ4=", "eZU8xcW/eJ4=")],
)
def test_urlsafe_b64decode_unpadded_with_padded_values(b64url_padded, b64):
    b64url_decoded = urlsafe_b64decode_unpadded(b64url_padded)

    assert base64.b64encode(b64url_decoded).decode("UTF-8") == b64


@pytest.mark.parametrize(
    "b64url, b64",
    [
        ("HT-sGfUaHj-rDA", "HT+sGfUaHj+rDA=="),
        ("X_uuRoHwt9_B6g", "X/uuRoHwt9/B6g=="),
        ("eZU8xcW_eJ4", "eZU8xcW/eJ4="),
        ("-OyhuDs6dAg", "+OyhuDs6dAg="),
        ("c3RyaW5n", "c3RyaW5n"),
    ],
)
def test_urlsafe_b64encode_unpadded(b64url, b64):
    assert urlsafe_b64encode_unpadded(base64.b64decode(b64)) == b64url
