# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import collections
import json
import logging

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

    def value_based_on_content_type(self, value, content_type=None):
        if content_type == self.CT_STRING:
            return value.decode('utf-8')
        elif value == b'':
            raise ValueError("Content type: '{0}' should not have an empty value".format(content_type))
        elif content_type == self.CT_DATE:
            return value.decode('utf-8')
        elif content_type == self.CT_JPEG \
                or content_type == self.CT_PNG:
            return value
        elif content_type == self.CT_JSON:
            return self.convert_to_dict(value)
        elif content_type == self.CT_INT:
            string_value = value.decode('utf-8')
            int_value = int(string_value)
            return int_value

        if logging.getLogger().propagate:
            logging.warning("Unknown type '{0}', attempting to parse it as a String".format(content_type))

        return value.decode('utf-8')

    def image_uri_based_on_content_type(self, value, content_type=None):
        if content_type == self.CT_JPEG:
            data = base64.b64encode(value).decode('utf-8')
            return 'data:image/jpeg;base64,{0}'.format(data)
        elif content_type == self.CT_PNG:
            data = base64.b64encode(value).decode('utf-8')
            return 'data:image/png;base64,{0}'.format(data)
        return value

    @staticmethod
    def convert_to_dict(byte_value):
        decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict, strict=False)
        value_to_decode = byte_value.decode()

        return decoder.decode(value_to_decode)
