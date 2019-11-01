# -*- coding: utf-8 -*-

from yoti_python_sdk.issuance_details import IssuanceDetails
from yoti_python_sdk.protobuf.share_public_api import ThirdPartyAttribute_pb2


class ExtraData(object):
    THIRD_PARTY_ATTRIBUTE = 6

    def __init__(self, proto):
        self.__attribute_issuance_details = None
        data_entries_list = proto.list

        for data_entry in data_entries_list:
            if (
                data_entry.type == self.THIRD_PARTY_ATTRIBUTE
                and self.__attribute_issuance_details is None
            ):
                attribute = ThirdPartyAttribute_pb2.ThirdPartyAttribute()
                attribute.MergeFromString(data_entry.value)
                self.__attribute_issuance_details = IssuanceDetails(attribute)

    @property
    def attribute_issuance_details(self):
        return self.__attribute_issuance_details
