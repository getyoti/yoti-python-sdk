# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import copy


class ThirdPartyAttributeExtension(object):
    THIRDPARTY_ATTRIBUTE = "THIRD_PARTY_ATTRIBUTE"

    def __init__(self):
        self.__extension = {}
        self.__extension["type"] = self.THIRDPARTY_ATTRIBUTE
        self.__extension["content"] = {"expiry_date": None, "definitions": []}

    def with_expiry_date(self, expiry_date):
        self.__extension["content"]["expiry_date"] = expiry_date.isoformat()
        return self

    def with_definitions(self, *names):
        self.__extension["content"]["definitions"].extend([{"name": s} for s in names])
        return self

    def build(self):
        return copy.deepcopy(self.__extension)
