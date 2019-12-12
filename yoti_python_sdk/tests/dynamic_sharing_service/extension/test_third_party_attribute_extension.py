# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from yoti_python_sdk.dynamic_sharing_service.extension.third_party_attribute_extension import (
    ThirdPartyAttributeExtension,
)


def test_should_create_extension():
    DEFINITION = "some_value"
    expiry_date = datetime(2019, 10, 30, 12, 10, 9, int(458e3))

    extension = (
        ThirdPartyAttributeExtension()
        .with_expiry_date(expiry_date)
        .with_definitions(DEFINITION)
        .build()
    )

    assert extension["type"] == ThirdPartyAttributeExtension.THIRDPARTY_ATTRIBUTE
    assert extension["content"]["expiry_date"] == "2019-10-30T12:10:09.458000"
    assert extension["content"]["definitions"][0]["name"] == DEFINITION


def test_with_definition_should_add_to_list():
    DEFINITION1 = "some_attribute"
    DEFINITION2 = "some_other_attribute"

    expiry_date = datetime(2019, 10, 30, 12, 10, 9, int(458e3))

    extension = (
        ThirdPartyAttributeExtension()
        .with_expiry_date(expiry_date)
        .with_definitions(DEFINITION1)
        .with_definitions(DEFINITION2)
        .build()
    )

    assert extension["type"] == ThirdPartyAttributeExtension.THIRDPARTY_ATTRIBUTE
    assert extension["content"]["expiry_date"] == "2019-10-30T12:10:09.458000"

    assert extension["content"]["definitions"][0]["name"] == DEFINITION1
    assert extension["content"]["definitions"][1]["name"] == DEFINITION2


def test_with_definition_should_add_multiple():
    DEFINITION1 = "some_attribute"
    DEFINITION2 = "some_other_attribute"

    expiry_date = datetime(2019, 10, 30, 12, 10, 9, int(458e3))

    extension = (
        ThirdPartyAttributeExtension()
        .with_expiry_date(expiry_date)
        .with_definitions(DEFINITION1, DEFINITION2)
        .build()
    )

    assert extension["type"] == ThirdPartyAttributeExtension.THIRDPARTY_ATTRIBUTE
    assert extension["content"]["expiry_date"] == "2019-10-30T12:10:09.458000"

    assert extension["content"]["definitions"][0]["name"] == DEFINITION1
    assert extension["content"]["definitions"][1]["name"] == DEFINITION2
