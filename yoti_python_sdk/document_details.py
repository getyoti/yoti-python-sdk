# -*- coding: utf-8 -*-
from . import date_parser


class DocumentDetails(object):
    def __init__(self, data):
        self.__parse_data(data)

    @property
    def document_type(self):
        return self.__document_type

    @property
    def issuing_country(self):
        return self.__issuing_country

    @property
    def document_number(self):
        return self.__document_number

    @property
    def expiration_date(self):
        return self.__dict__.get("_DocumentDetails__expiration_date", None)

    @property
    def issuing_authority(self):
        return self.__dict__.get("_DocumentDetails__issuing_authority", None)

    def __parse_data(self, data):
        data = data.split(" ")
        if len(data) < 3 or "" in data:
            raise ValueError("Invalid value for DocumentDetails")

        self.__document_type = data[0]
        self.__issuing_country = data[1]
        self.__document_number = data[2]
        if len(data) > 3:
            date = data[3]
            if date != "-":
                self.__expiration_date = date_parser.from_iso_format(date)
        if len(data) > 4:
            self.__issuing_authority = data[4]
