# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cryptography.fernet import base64

import yoti_python_sdk.protobuf.v1.attribute_public_api.list_pb2 as attrpubapi
import yoti_python_sdk.protobuf.v1.common_public_api.encrypted_data_pb2 as compubapi


class Protobuf(object):
    CT_UNDEFINED = 0  # should not be seen, and is used as an error placeholder
    CT_STRING = 1  # UTF-8 encoded text.
    CT_JPEG = 2  # standard .jpeg image.
    CT_DATE = 3  # string in RFC3339 format (YYYY-MM-DD)
    CT_PNG = 4  # standard .png image

    def current_user(self, receipt):
        if receipt.get('other_party_profile_content') is None:
            raise ValueError('The receipt has invalid data')
        profile_content = receipt['other_party_profile_content']
        decoded_profile_content = base64.b64decode(profile_content)

        merged_user = compubapi.EncryptedData()
        merged_user.MergeFromString(decoded_profile_content)
        return merged_user

    def attribute_list(self, data):
        attribute_list = attrpubapi.AttributeList()
        attribute_list.MergeFromString(data)
        return attribute_list

    def value_based_on_content_type(self, value, content_type=None):
        if content_type == self.CT_UNDEFINED:
            raise TypeError('Wrong content type')
        elif content_type == self.CT_STRING:
            return value.decode('utf-8')
        elif content_type == self.CT_JPEG:
            data = base64.b64encode(value).decode('utf-8')
            return 'data:image/jpeg;base64,{0}'.format(data)
        elif content_type == self.CT_DATE:
            return value.decode('utf-8')
        elif content_type == self.CT_PNG:
            data = base64.b64encode(value).decode('utf-8')
            return 'data:image/png;base64,{0}'.format(data)
        return value
