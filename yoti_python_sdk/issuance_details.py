# -*- coding: utf-8 -*-


class IssuanceDetails(object):
    def __init__(self, data_entry):
        self.__token = data_entry.issuance_token.decode()
        if (
            data_entry.issuing_attributes.expiry_date != ""
            and data_entry.issuing_attributes.expiry_date is not None
        ):
            self.__expiry_date = data_entry.issuing_attributes.expiry_date
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
