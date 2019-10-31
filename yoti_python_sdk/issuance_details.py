# -*- coding: utf-8 -*-


class IssuanceDetails(object):
    def __init__(self, data_entry):
        self.__token = getattr(data_entry.value, "issuance_token").decode()
        self.__expiry_date = data_entry.value.issuing_attributes.expiry_date
        self.__attributes = data_entry.value.issuing_attributes.definitions

    @property
    def token(self):
        return self.__token

    @property
    def attributes(self):
        return self.__attributes

    @property
    def expiry_date(self):
        return self.__expiry_date
