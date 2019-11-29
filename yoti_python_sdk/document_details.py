# -*- coding: utf-8 -*-
import re

from . import date_parser


class DocumentDetails(object):
    VALIDATION_REGEX = re.compile("^[A-Za-z_]* [A-Za-z]{3} [A-Za-z0-9]{1}.*$")

    def __init__(self, data):
        # Non-required attributes default to None
        self.__expiration_date = None
        self.__issuing_authority = None

        self.__validate_data(data)
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
        return self.__expiration_date

    @property
    def issuing_authority(self):
        return self.__issuing_authority

    def __validate_data(self, data):
        if self.VALIDATION_REGEX.search(data):
            return
        else:
            raise ValueError("Invalid value for DocumentDetails")

    def __parse_data(self, data):
        data = data.split()

        self.__document_type = data[0]
        self.__issuing_country = data[1]
        self.__document_number = data[2]
        if len(data) > 3:
            date = data[3]
            if date != "-":
                self.__expiration_date = date_parser.date_from_string(date)
        if len(data) > 4:
            self.__issuing_authority = data[4]
