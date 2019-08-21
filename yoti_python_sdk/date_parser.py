# -*- coding: utf-8 -*-

import datetime


def from_iso_format(string):
    parts = [int(a) for a in string.split("-")]

    if len(parts) != 3:
        raise ValueError

    return datetime.date(parts[0], parts[1], parts[2])
