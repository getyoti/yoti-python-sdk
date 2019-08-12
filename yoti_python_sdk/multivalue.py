# -*- coding: utf-8 -*-
from yoti_python_sdk.protobuf import protobuf


def parse(multi_value_bytes):
    from yoti_python_sdk import (
        attribute_parser,
    )  # needed here (and not above) for Python 2.7 & 3.4 dependency handling

    proto = protobuf.Protobuf()
    multi_value_list = []
    parsed_multi_value = proto.multi_value(multi_value_bytes)

    for multi_value_item in parsed_multi_value.values:
        multi_value_list.append(
            attribute_parser.value_based_on_content_type(
                multi_value_item.data, multi_value_item.content_type
            )
        )

    return multi_value_list


def filter_values(values, type_to_filter):
    return tuple(filter(lambda v: isinstance(v, type_to_filter), values))
