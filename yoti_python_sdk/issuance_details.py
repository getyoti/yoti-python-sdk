# -*- coding: utf-8 -*-

from datetime import datetime
import re


class IssuanceDetails(object):
    def __init__(self, data_entry):
        self.__token = data_entry.issuance_token.decode()
        if (
            data_entry.issuing_attributes.expiry_date != ""
            and data_entry.issuing_attributes.expiry_date is not None
        ):
            time_split = re.split("[^0-9]", data_entry.issuing_attributes.expiry_date)
            print("!DEBUG! %s" % time_split)
            assert len(time_split) >= 7
            year = int(time_split[0])
            month = int(time_split[1])
            day = int(time_split[2])
            hour = int(time_split[3])
            minute = int(time_split[4])
            second = int(time_split[5])
            microsecond = int(float("0." + time_split[6]) * 1e6)
            self.__expiry_date = datetime(
                year, month, day, hour, minute, second, microsecond
            )
            # TODO: Refactor time parser into own method
        else:
            self.__expiry_date = None
        self.__attributes = data_entry.issuing_attributes.definitions

    @property
    def token(self):
        return self.__token

    @property
    def attributes(self):
        return self.__attributes

    @property
    def expiry_date(self):
        return self.__expiry_date
