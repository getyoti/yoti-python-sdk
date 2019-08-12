# -*- coding: utf-8 -*-
from os.path import abspath, dirname, join

from yoti_python_sdk import attribute_parser
from yoti_python_sdk.protobuf import protobuf
from yoti_python_sdk.tests import file_helper

FIXTURES_DIR = join(dirname(abspath(__file__)), "fixtures")
ATTRIBUTE_DOCUMENT_IMAGES = join(FIXTURES_DIR, "attribute_document_images.txt")


def get_attribute_from_base64_text(file_path):
    attribute_bytes = file_helper.get_file_bytes(file_path)

    return protobuf.Protobuf().attribute(attribute_bytes)


def parse_multi_value():
    multi_value_proto_attribute = get_attribute_from_base64_text(
        ATTRIBUTE_DOCUMENT_IMAGES
    )

    return attribute_parser.value_based_on_content_type(
        multi_value_proto_attribute.value, multi_value_proto_attribute.content_type
    )
