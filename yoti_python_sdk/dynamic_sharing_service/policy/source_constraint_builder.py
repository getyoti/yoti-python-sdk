# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.config import (
    ANCHOR_VALUE_PASSPORT,
    ANCHOR_VALUE_PASS_CARD,
    ANCHOR_VALUE_NATIONAL_ID,
    ANCHOR_VALUE_DRIVING_LICENCE,
)

from .wanted_anchor_builder import WantedAnchorBuilder


class SourceConstraintBuilder(object):
    def __init__(self):
        self.__soft_preference = False
        self.__anchors = []

    def with_soft_preference(self, value=True):
        """
        :param value: If true, this will be treated as a soft preference, otherwise
                      this will be treated as a hard requirement
        """
        self.__soft_preference = value
        return self

    def with_anchor(self, anchor):
        """
        :param anchor: Add an anchor to the source constraint.
        It is recommended to use the other helper methods instead of this one
        """
        self.__anchors.append(anchor)
        return self

    def with_anchor_by_name(self, value, subtype=""):
        """
        :param value: The type of anchor wanted, represented by a string
        :param subtype: The subtype information for the anchor as a string
        """
        anchor = WantedAnchorBuilder().with_value(value).with_subtype(subtype).build()
        return self.with_anchor(anchor)

    def with_passport(self, subtype=""):
        """
        :param subtype: Subtype information as a string
        """
        return self.with_anchor_by_name(ANCHOR_VALUE_PASSPORT, subtype)

    def with_national_id(self, subtype=""):
        """
        :param subtype: Subtype information as a string
        """
        return self.with_anchor_by_name(ANCHOR_VALUE_NATIONAL_ID, subtype)

    def with_passcard(self, subtype=""):
        """
        :param subtype: Subtype information as a string
        """
        return self.with_anchor_by_name(ANCHOR_VALUE_PASS_CARD, subtype)

    def with_driving_licence(self, subtype=""):
        """
        :param subtype: Subtype information as a string
        """
        return self.with_anchor_by_name(ANCHOR_VALUE_DRIVING_LICENCE, subtype)

    def build(self):
        """
        :returns: A dict describing the source constraint
        """
        return {
            "type": "SOURCE",
            "preferred_sources": {
                "soft_preference": self.__soft_preference,
                "anchors": self.__anchors,
            },
        }
