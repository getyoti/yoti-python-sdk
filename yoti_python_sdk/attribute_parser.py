# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import collections
import json
import logging

from yoti_python_sdk import multivalue
from yoti_python_sdk.protobuf.protobuf import Protobuf


def value_based_on_content_type(value, content_type=None):
    from yoti_python_sdk.image import Image

    if content_type == Protobuf.CT_STRING:
        return value.decode("utf-8")
    elif value == b"":
        raise ValueError(
            "Content type: '{0}' should not have an empty value".format(content_type)
        )
    elif content_type == Protobuf.CT_DATE:
        return value.decode("utf-8")
    elif content_type in Image.allowed_types():
        return Image(value, content_type)
    elif content_type == Protobuf.CT_JSON:
        return convert_to_dict(value)
    elif content_type == Protobuf.CT_INT:
        string_value = value.decode("utf-8")
        int_value = int(string_value)
        return int_value
    elif content_type == Protobuf.CT_MULTI_VALUE:
        return tuple(multivalue.parse(value))

    if logging.getLogger().propagate:
        logging.warning(
            "Unknown type '{0}', attempting to parse it as a String".format(
                content_type
            )
        )

    return value.decode("utf-8")


def convert_to_dict(byte_value):
    decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict, strict=False)
    value_to_decode = byte_value.decode()

    return decoder.decode(value_to_decode)
