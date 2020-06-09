# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

import pytest
import pytz

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
    assert extension["content"]["expiry_date"] == "2019-10-30T12:10:09.458Z"
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
    assert extension["content"]["expiry_date"] == "2019-10-30T12:10:09.458Z"

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
    assert extension["content"]["expiry_date"] == "2019-10-30T12:10:09.458Z"

    assert extension["content"]["definitions"][0]["name"] == DEFINITION1
    assert extension["content"]["definitions"][1]["name"] == DEFINITION2


@pytest.mark.parametrize(
    "expiry_date, expected_value",
    [
        (
            datetime(2051, 1, 13, 19, 50, 53, 1, tzinfo=pytz.utc),
            "2051-01-13T19:50:53.000Z",
        ),
        (
            datetime(2026, 2, 2, 22, 4, 5, 123, tzinfo=pytz.utc),
            "2026-02-02T22:04:05.000Z",
        ),
        (
            datetime(2051, 4, 13, 19, 50, 53, 999, tzinfo=pytz.utc),
            "2051-04-13T19:50:53.000Z",
        ),
        (
            datetime(2026, 1, 31, 22, 4, 5, 1232, tzinfo=pytz.utc),
            "2026-01-31T22:04:05.001Z",
        ),
        (
            datetime(2026, 1, 31, 22, 4, 5, 17777, tzinfo=pytz.utc),
            "2026-01-31T22:04:05.017Z",
        ),
        (
            datetime(2019, 10, 30, 12, 10, 9, int(458e3), tzinfo=pytz.utc),
            "2019-10-30T12:10:09.458Z",
        ),
        (
            datetime(2026, 1, 2, 22, 4, 5, 123456, tzinfo=pytz.utc),
            "2026-01-02T22:04:05.123Z",
        ),
    ],
)
def test_should_format_utc_expiry_dates_correctly(expiry_date, expected_value):
    DEFINITION = "some_value"

    extension = (
        ThirdPartyAttributeExtension()
        .with_expiry_date(expiry_date)
        .with_definitions(DEFINITION)
        .build()
    )

    assert extension["content"]["expiry_date"] == expected_value


@pytest.mark.parametrize(
    "expiry_date, tz_name",
    [
        (datetime(2030, 6, 6, 8, 0, 0, 0), "US/Eastern",),
        (datetime(2030, 6, 6, 15, 0, 0, 0), "Europe/Moscow",),
        (datetime(2030, 6, 6, 7, 0, 0, 0), "America/Jamaica",),
        (datetime(2030, 6, 6, 23, 0, 0, 0), "Etc/GMT-11"),
        (datetime(2030, 6, 6, 7, 0, 0, 0), "Etc/GMT+5"),
        # In order to conform with the POSIX style, those zones beginning
        # with "Etc/GMT" have their sign reversed from what most people expect. In this style, zones west of GMT have
        # a positive sign and those east have a negative sign.
    ],
)
def test_should_format_localized_expiry_dates(expiry_date, tz_name):
    DEFINITION = "some_value"

    tz = pytz.timezone(tz_name)
    localized_expiry_date = tz.localize(expiry_date)

    extension = (
        ThirdPartyAttributeExtension()
        .with_expiry_date(localized_expiry_date)
        .with_definitions(DEFINITION)
        .build()
    )

    assert extension["content"]["expiry_date"] == "2030-06-06T12:00:00.000Z"
