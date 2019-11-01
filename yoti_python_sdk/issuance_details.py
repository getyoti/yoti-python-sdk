# -*- coding: utf-8 -*-

from yoti_python_sdk.protobuf.protobuf import Protobuf


class IssuanceDetails(object):
    def __init__(self, data_entry):
        if isinstance(data_entry.value, bytes):
            value = Protobuf.thirdparty_attribute(data_entry.value)
        else:
            value = data_entry.value
        self.__token = value.issuance_token.decode()
        if (
            value.issuing_attributes.expiry_date != ""
            and value.issuing_attributes.expiry_date is not None
        ):
            self.__expiry_date = value.issuing_attributes.expiry_date
        else:
            self.__expiry_date = None
        self.__attributes = value.issuing_attributes.definitions

    @property
    def token(self):
        return self.__token

    @property
    def attributes(self):
        return self.__attributes

    @property
    def expiry_date(self):
        return self.__expiry_date
