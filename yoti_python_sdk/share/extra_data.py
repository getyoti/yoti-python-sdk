# -*- coding: utf-8 -*-

from yoti_python_sdk.issuance_details import IssuanceDetails


class ExtraData(object):
    THIRD_PARTY_ATTRIBUTE = 6

    def __init__(self, data_entries_list):
        self.__attribute_issuance_details = None

        for data_entry in data_entries_list:
            if (
                data_entry.type == self.THIRD_PARTY_ATTRIBUTE
                and self.__attribute_issuance_details is None
            ):
                self.__attribute_issuance_details = IssuanceDetails(data_entry)

    @property
    def attribute_issuance_details(self):
        return self.__attribute_issuance_details
