import pytz
import pytest

from datetime import date, datetime

from yoti_python_sdk import date_parser


@pytest.mark.parametrize(
    "input_value, expected_type, expected_value",
    [
        ("1927-12-26", date, date(year=1927, month=12, day=26)),
        ("1970-04-09", date, date(year=1970, month=4, day=9)),
    ],
)
def test_date_from_string_valid(input_value, expected_type, expected_value):
    result = date_parser.date_from_string(input_value)

    assert isinstance(result, expected_type) is True
    assert result == expected_value


@pytest.mark.parametrize(
    "input_value", ["1920, 1st of the Month!", "Why would we pass a string?"]
)
def test_date_from_string_throws_error_if_invalid_format(input_value):
    with pytest.raises(ValueError) as ex:
        date_parser.date_from_string(input_value)

    assert "does not match format" in str(ex.value)


@pytest.mark.parametrize(
    "input_value, expected_type, expected_value",
    [
        (
            "1927-12-26T12:05:30Z",
            datetime,
            datetime(
                year=1927,
                month=12,
                day=26,
                hour=12,
                minute=5,
                second=30,
                tzinfo=pytz.utc,
            ),
        ),
        (
            "1970-04-09T02:49:07Z",
            datetime,
            datetime(
                year=1970, month=4, day=9, hour=2, minute=49, second=7, tzinfo=pytz.utc
            ),
        ),
    ],
)
def test_datetime_from_string_valid(input_value, expected_type, expected_value):
    result = date_parser.datetime_from_string(input_value)

    assert isinstance(result, expected_type) is True
    assert result == expected_value


@pytest.mark.parametrize(
    "input_value", ["1920, 1st of the Month!", "Why would we pass a string?"]
)
def test_datetime_from_string_throws_error_if_invalid_format(input_value):
    with pytest.raises(ValueError) as ex:
        date_parser.datetime_from_string(input_value)

    assert "does not match format" in str(ex.value)


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        (
            1575030722,
            datetime(
                year=2019,
                month=11,
                day=29,
                hour=12,
                minute=32,
                second=2,
                tzinfo=pytz.utc,
            ),
        ),
        (
            -3829273028,
            datetime(
                year=1848,
                month=8,
                day=27,
                hour=17,
                minute=2,
                second=52,
                tzinfo=pytz.utc,
            ),
        ),
    ],
)
def test_parse_timestamp_from_seconds(input_value, expected_value):
    result = date_parser.parse_from_timestamp(input_value)

    assert result == expected_value


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        (
            1575030722387,
            datetime(
                year=2019,
                month=11,
                day=29,
                hour=12,
                minute=32,
                second=2,
                microsecond=387000,
                tzinfo=pytz.utc,
            ),
        ),
        (
            -3829273028324,
            datetime(
                year=1848,
                month=8,
                day=27,
                hour=17,
                minute=2,
                second=51,
                microsecond=676000,
                tzinfo=pytz.utc,
            ),
        ),
    ],
)
def test_parse_timestamp_from_milliseconds(input_value, expected_value):
    result = date_parser.parse_timestamp_from_milliseconds(input_value)

    assert result == expected_value


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        (
            1575030722387678,
            datetime(
                year=2019,
                month=11,
                day=29,
                hour=12,
                minute=32,
                second=2,
                microsecond=387678,
                tzinfo=pytz.utc,
            ),
        ),
        (
            -3829273028324789,
            datetime(
                year=1848,
                month=8,
                day=27,
                hour=17,
                minute=2,
                second=51,
                microsecond=675211,
                tzinfo=pytz.utc,
            ),
        ),
    ],
)
def test_parse_timestamp_from_microseconds(input_value, expected_value):
    result = date_parser.parse_timestamp_from_microseconds(input_value)

    assert result == expected_value
