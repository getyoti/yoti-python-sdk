# -*- coding: utf-8 -*-

from yoti_python_sdk import date_parser
import base64


class IssuanceDetails(object):
    def __init__(self, data_entry):
        self.__token = base64.b64encode(data_entry.issuance_token)
        self.__expiry_date = date_parser.datetime_with_microsecond(
            data_entry.issuing_attributes.expiry_date
        )
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
