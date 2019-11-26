# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cryptography.fernet import base64
from yoti_python_sdk.protobuf.attribute_public_api import Attribute_pb2, List_pb2
from yoti_python_sdk.protobuf.common_public_api import EncryptedData_pb2
from yoti_python_sdk.protobuf.share_public_api import ExtraData_pb2
from yoti_python_sdk.protobuf.share_public_api import ThirdPartyAttribute_pb2


class Protobuf(object):
    CT_UNDEFINED = 0  # should not be seen, and is used as an error placeholder
    CT_STRING = 1  # UTF-8 encoded text
    CT_JPEG = 2  # standard .jpeg image
    CT_DATE = 3  # string in RFC3339 format (YYYY-MM-DD)
    CT_PNG = 4  # standard .png image
    CT_JSON = 5  # value encoded using JSON
    CT_MULTI_VALUE = 6  # allows a list of values
    CT_INT = 7  # int value

    @staticmethod
    def current_user(receipt):
        if receipt.get('other_party_profile_content') is None or receipt.get('other_party_profile_content') == '':
            return None

        profile_content = receipt['other_party_profile_content']
        decoded_profile_content = base64.b64decode(profile_content)

        merged_user = EncryptedData_pb2.EncryptedData()
        merged_user.MergeFromString(decoded_profile_content)
        return merged_user

    @staticmethod
    def current_application(receipt):
        if receipt.get("profile_content") is None or receipt.get("profile_content") == '':
            return None

        application_content = receipt["profile_content"]
        decoded_application_content = base64.b64decode(application_content)

        merged_application = EncryptedData_pb2.EncryptedData()
        merged_application.MergeFromString(decoded_application_content)

        return merged_application

    @staticmethod
    def attribute_list(data):
        attribute_list = List_pb2.AttributeList()
        attribute_list.MergeFromString(data)
        return attribute_list

    @staticmethod
    def anchor(data):
        anchor = Attribute_pb2.Anchor()
        anchor.MergeFromString(data)
        return anchor

    @staticmethod
    def attribute(data):
        attribute = Attribute_pb2.Attribute()
        attribute.MergeFromString(data)
        return attribute

    @staticmethod
    def multi_value(data):
        multi_value = Attribute_pb2.MultiValue()
        multi_value.MergeFromString(data)
        return multi_value

    @staticmethod
    def extra_data(receipt):
        if receipt.get("extra_data_content") is None or receipt.get("extra_data_content") == '':
            return None

        extra_data_content = receipt["extra_data_content"]
        extra_data_content = base64.b64decode(extra_data_content)

        extra_data = EncryptedData_pb2.EncryptedData()
        extra_data.MergeFromString(extra_data_content)
        return extra_data

    @staticmethod
    def thirdparty_attribute(data):
        thirdparty_attribute = ThirdPartyAttribute_pb2.ThirdPartyAttribute()
        thirdparty_attribute.MergeFromString(data)
        return thirdparty_attribute
