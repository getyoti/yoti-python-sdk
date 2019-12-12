# -*- coding: utf-8 -*-

from yoti_python_sdk.attribute_issuance_details import AttributeIssuanceDetails
from yoti_python_sdk.protobuf.share_public_api import ThirdPartyAttribute_pb2
from yoti_python_sdk.protobuf.share_public_api import ExtraData_pb2


class ExtraData(object):
    THIRD_PARTY_ATTRIBUTE = 6

    def __init__(self, raw):
        self.__attribute_issuance_details = None
        proto = ExtraData_pb2.ExtraData()
        proto.MergeFromString(raw)
        data_entries_list = proto.list

        for data_entry in data_entries_list:
            if (
                data_entry.type == self.THIRD_PARTY_ATTRIBUTE
                and self.__attribute_issuance_details is None
            ):
                attribute = ThirdPartyAttribute_pb2.ThirdPartyAttribute()
                attribute.MergeFromString(data_entry.value)
                self.__attribute_issuance_details = AttributeIssuanceDetails(attribute)

    @property
    def attribute_issuance_details(self):
        return self.__attribute_issuance_details
