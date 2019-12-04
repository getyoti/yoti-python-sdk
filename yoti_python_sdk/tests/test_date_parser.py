# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from yoti_python_sdk import date_parser
import pytest


@pytest.mark.parametrize(
    "string,expected",
    [
        ("2006-11-02T15:04:05.010Z", datetime(2006, 11, 2, 15, 4, 5, 10000)),
        ("2006-09-02T15:04:05.010Z", datetime(2006, 9, 2, 15, 4, 5, 10000)),
        ("2006-9-02T15:04:05.010Z", datetime(2006, 9, 2, 15, 4, 5, 10000)),
        ("200006-11-02T15:04:05.010Z", None),
        ("2006-13-02T15:04:05.010Z", None),
        ("2006-09-31T15:04:05.010Z", None),
        ("2006-11-02T15:04:05", None),
        ("2006-11-02T15:04", None),
        ("2006-11-02T15", None),
        ("2006-11-02", None),
        ("2006-11", None),
        ("2006", None),
        ("This is not a date", None),
    ],
)
def test_datetime_with_microsecond_should_handle_missing_and_invalid(string, expected):
    output = date_parser.datetime_with_microsecond(string)
    assert output == expected
