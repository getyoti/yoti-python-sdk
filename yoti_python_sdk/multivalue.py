# -*- coding: utf-8 -*-
from yoti_python_sdk import attribute_parser
from yoti_python_sdk.protobuf import protobuf


def parse(multi_value_bytes):
    proto = protobuf.Protobuf()
    multi_value_list = []
    parsed_multi_value = proto.multi_value(multi_value_bytes)

    for multi_value_item in parsed_multi_value.values:
        value = attribute_parser.value_based_on_content_type(multi_value_item.data, multi_value_item.content_type)

        if value.content_type == proto.CT_MULTI_VALUE:
            multi_value_list.append(parse(value))
        else:
            multi_value_list.append(value)

    return multi_value_list


def filter_values(values, type_to_filter):
    return list(filter(lambda v: isinstance(v, type_to_filter), values))
