# -*- coding: utf-8 -*-

from datetime import datetime, date
import logging
import re


ERROR_PARSING_DATE = "Error parsing date"


def from_iso_format(string):
    parts = [int(a) for a in string.split("-")]

    if len(parts) != 3:
        raise ValueError

    return date(parts[0], parts[1], parts[2])


def datetime_with_microsecond(string):
    # Python2 does not have a way of parsing date formats.
    # Deprecate this once Python2 support is dropped.
    time_split = re.split("[^0-9]", string)
    parts = len(time_split)
    if parts <= 6:
        if logging.getLogger().propagate:
            logging.warning(ERROR_PARSING_DATE)
        return None

    try:
        year = int(time_split[0])
        month = int(time_split[1])
        day = int(time_split[2])
        hour = int(time_split[3])
        minute = int(time_split[4])
        second = int(time_split[5])
        microsecond = int(round(float("0." + time_split[6]) * 1e6))
        return datetime(year, month, day, hour, minute, second, microsecond)
    except ValueError:
        if logging.getLogger().propagate:
            logging.warning(ERROR_PARSING_DATE)
        return None
