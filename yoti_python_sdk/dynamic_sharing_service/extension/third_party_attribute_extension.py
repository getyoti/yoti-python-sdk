# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import copy

import pytz


class ThirdPartyAttributeExtension(object):
    THIRDPARTY_ATTRIBUTE = "THIRD_PARTY_ATTRIBUTE"

    def __init__(self):
        self.__extension = {
            "type": self.THIRDPARTY_ATTRIBUTE,
            "content": {"expiry_date": None, "definitions": []},
        }

    def with_expiry_date(self, expiry_date):
        """
        :param expiry_date: Expiry date for the attribute. If no timezone info is provided, UTC will be used.
        :type expiry_date: datetime
        """
        if expiry_date.tzinfo is None:
            expiry_date = expiry_date.replace(tzinfo=pytz.UTC)

        utc_time = expiry_date.astimezone(pytz.utc)
        rfc_3339_milliseconds = utc_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
        self.__extension["content"]["expiry_date"] = rfc_3339_milliseconds + "Z"
        return self

    def with_definitions(self, *names):
        """
        :param names: attribute definitions
        :type names: str or list[str]
        """
        self.__extension["content"]["definitions"].extend([{"name": s} for s in names])
        return self

    def build(self):
        """
        Builds the object

        :return: the third party attribute
        :rtype: ThirdPartyAttributeExtension
        """
        return copy.deepcopy(self.__extension)
