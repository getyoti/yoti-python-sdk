# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cryptography.fernet import base64
from yoti_python_sdk.protobuf.attribute_public_api import Attribute_pb2, List_pb2
from yoti_python_sdk.protobuf.common_public_api import EncryptedData_pb2


class Protobuf(object):
    CT_UNDEFINED = 0  # should not be seen, and is used as an error placeholder
    CT_STRING = 1  # UTF-8 encoded text
    CT_JPEG = 2  # standard .jpeg image
    CT_DATE = 3  # string in RFC3339 format (YYYY-MM-DD)
    CT_PNG = 4  # standard .png image
    CT_JSON = 5  # value encoded using JSON
    CT_INT = 6  # int value
    CT_MULTI_VALUE = 7  # allows a list of values

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
    def attribute_list(data):
        attribute_list = List_pb2.AttributeList()
        attribute_list.MergeFromString(data)
        return attribute_list

    @staticmethod
    def anchor(data):
        anchor = Attribute_pb2.Anchor()
        anchor.MergeFromString(data)
        return anchor
