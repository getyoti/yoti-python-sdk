import pytz
import pytest
import iso8601

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
    with pytest.raises(iso8601.iso8601.ParseError) as ex:
        date_parser.datetime_from_string(input_value)

    assert "Unable to parse date string" in str(ex.value)


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


@pytest.mark.parametrize(
    "string, expected",
    [
        ("2006-01-02T22:04:05Z", datetime(2006, 1, 2, 22, 4, 5, 0, pytz.utc)),
        (
            "2006-01-02T22:04:05.1Z",
            datetime(2006, 1, 2, 22, 4, 5, int(100e3), pytz.utc),
        ),
        (
            "2006-01-02T22:04:05.12Z",
            datetime(2006, 1, 2, 22, 4, 5, int(120e3), pytz.utc),
        ),
        (
            "2006-01-02T22:04:05.123Z",
            datetime(2006, 1, 2, 22, 4, 5, int(123e3), pytz.utc),
        ),
        ("2006-01-02T22:04:05.1234Z", datetime(2006, 1, 2, 22, 4, 5, 123400, pytz.utc)),
        (
            "2006-01-02T22:04:05.12345Z",
            datetime(2006, 1, 2, 22, 4, 5, 123450, pytz.utc),
        ),
        (
            "2006-01-02T22:04:05.123456Z",
            datetime(2006, 1, 2, 22, 4, 5, 123456, pytz.utc),
        ),
        (
            "2002-10-02T10:00:00-05:00",
            datetime(2002, 10, 2, 10, 0, 0, 0, pytz.FixedOffset(-5 * 60)),
        ),
        (
            "2002-10-02T10:00:00+11:00",
            datetime(2002, 10, 2, 10, 0, 0, 0, pytz.FixedOffset(11 * 60)),
        ),
    ],
)
def test_datetime_with_microsecond_should_handle_all_rfc3339(string, expected):
    output = date_parser.datetime_from_string(string)
    assert output.astimezone(pytz.utc) == expected.astimezone(pytz.utc)
