# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.dynamic_sharing_service.extension.extension_builder import (
    ExtensionBuilder,
)


def test_build_simple_extension():
    EXTENSION_TYPE = "TEST"
    EXTENSION_CONTENT = 99

    extension = (
        ExtensionBuilder()
        .with_extension_type(EXTENSION_TYPE)
        .with_content(EXTENSION_CONTENT)
        .build()
    )

    assert extension["type"] == EXTENSION_TYPE
    assert extension["content"] == EXTENSION_CONTENT
