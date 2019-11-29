# -*- coding: utf-8 -*-

import pytz
import datetime


RFC_3999_DATE_FORMAT = "%Y-%m-%d"
RFC_3999_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def parse_date(date_string, format_string):
    """
    Parse a date string into datetime.datetime object, using the specified format string

    :param date_string: the raw date string
    :param format_string: the format used to parse the date string
    :return: datetime.datetime
    """
    return datetime.datetime.strptime(date_string, format_string).replace(
        tzinfo=pytz.utc
    )


def date_from_string(date_string):
    """
    Parse a date string into datetime.date object, using RFC_3999 format

    :param date_string: the raw date string
    :return: datetime.date
    """
    return parse_date(date_string, RFC_3999_DATE_FORMAT).date()


def datetime_from_string(date_string):
    """
    Parse a date string into datetime.datetime object, using RFC_3999 format

    :param date_string: the raw date string
    :return: datetime.datetime
    """
    return parse_date(date_string, RFC_3999_DATETIME_FORMAT)


def parse_from_timestamp(timestamp, division=1):
    """
    Parses a timestamp into the number of seconds since epoch, dividing the timestamp by supplied
    float

    :param timestamp: the timestamp
    :param division: the number to divide the timestamp by (default of 1, or no division)
    :return: datetime.datetime
    """
    return datetime.datetime.utcfromtimestamp(timestamp / float(division)).replace(
        tzinfo=pytz.utc
    )


def parse_timestamp_from_seconds(timestamp):
    """
    Parses a timestamp of number of seconds since epoch into datetime.datetime

    :param timestamp: the timestamp
    :return: datetime.datetime
    """
    return parse_from_timestamp(timestamp)


def parse_timestamp_from_milliseconds(timestamp):
    """
    Parses a timestamp of number of milliseconds since epoch into datetime.datetime

    :param timestamp: the timestamp
    :return: datetime.datetime
    """
    return parse_from_timestamp(timestamp, division=1000)


def parse_timestamp_from_microseconds(timestamp):
    """
    Parses a timestamp of number of microseconds since epoch into datetime.datetime

    :param timestamp: the timestamp
    :return: datetime.datetime
    """
    return parse_from_timestamp(timestamp, division=1000000)
