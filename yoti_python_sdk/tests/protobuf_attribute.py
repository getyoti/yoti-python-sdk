# -*- coding: utf-8 -*-
from yoti_python_sdk.protobuf.v1.protobuf import Protobuf


class ProtobufAttribute(object):
    name = ""
    value = ""
    anchors = ""
    content_type = Protobuf.CT_UNDEFINED

    def __init__(self, name, value, anchors, content_type):
        self.name = name
        self.value = value
        self.anchors = anchors
        self.content_type = content_type
