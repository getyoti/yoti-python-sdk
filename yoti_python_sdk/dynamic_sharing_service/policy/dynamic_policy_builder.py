# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from yoti_python_sdk import config

from .wanted_attribute_builder import WantedAttributeBuilder

"""
Builder for DynamicPolicy
"""


class DynamicPolicyBuilder(object):
    SELFIE_AUTH_TYPE = 1
    PIN_AUTH_TYPE = 2

    def __init__(self):
        self.__wanted_attributes = {}
        self.__wanted_auth_types = {}
        self.__is_wanted_remember_me = False

    """
    @param wanted_attribute
    """

    def with_wanted_attribute(self, wanted_attribute):
        key = (
            wanted_attribute["derivation"]
            if wanted_attribute.get("derivation", False)
            else wanted_attribute["name"]
        )
        self.__wanted_attributes[key] = wanted_attribute
        return self

    """
    @param wanted_name The name of the attribute to include
    """

    def with_wanted_attribute_by_name(self, wanted_name):
        attribute = WantedAttributeBuilder().with_name(wanted_name).build()
        return self.with_wanted_attribute(attribute)

    def with_family_name(self):
        return self.with_wanted_attribute_by_name(config.ATTRIBUTE_FAMILY_NAME)

    def with_given_names(self):
        return self.with_wanted_attribute_by_name(config.ATTRIBUTE_GIVEN_NAMES)

    def with_full_name(self):
        return self.with_wanted_attribute_by_name(config.ATTRIBUTE_FULL_NAME)

    def with_date_of_birth(self):
        return self.with_wanted_attribute_by_name(config.ATTRIBUTE_DATE_OF_BIRTH)

    def with_age_derived_attribute(self, derivation):
        attribute = (
            WantedAttributeBuilder()
            .with_name(config.ATTRIBUTE_DATE_OF_BIRTH)
            .with_derivation(derivation)
            .build()
        )
        return self.with_wanted_attribute(attribute)

    def with_age_over(self, age):
        assert self.__is_number(age)
        return self.with_age_derived_attribute(config.ATTRIBUTE_AGE_OVER + str(age))

    def with_age_under(self, age):
        assert self.__is_number(age)
        return self.with_age_derived_attribute(config.ATTRIBUTE_AGE_UNDER + str(age))

    def with_gender(self):
        return self.with_wanted_attribute_by_name(config.ATTRIBUTE_GENDER)

    def with_postal_address(self):
        return self.with_wanted_attribute_by_name(config.ATTRIBUTE_POSTAL_ADDRESS)

    def with_structured_postal_address(self):
        return self.with_wanted_attribute_by_name(
            config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS
        )

    def with_nationality(self):
        return self.with_wanted_attribute_by_name(config.ATTRIBUTE_NATIONALITY)

    def with_phone_number(self):
        return self.with_wanted_attribute_by_name(config.ATTRIBUTE_PHONE_NUMBER)

    def with_selfie(self):
        return self.with_wanted_attribute_by_name(config.ATTRIBUTE_SELFIE)

    def with_email(self):
        return self.with_wanted_attribute_by_name(config.ATTRIBUTE_EMAIL_ADDRESS)

    def with_document_details(self):
        return self.with_wanted_attribute_by_name(config.ATTRIBUTE_DOCUMENT_DETAILS)

    """
    @param wanted_auth_type
    """

    def with_wanted_auth_type(self, wanted_auth_type, wanted=True):
        self.__wanted_auth_types[wanted_auth_type] = wanted
        return self

    def with_selfie_auth(self, wanted=True):
        return self.with_wanted_auth_type(self.SELFIE_AUTH_TYPE, wanted)

    def with_pin_auth(self, wanted=True):
        return self.with_wanted_auth_type(self.PIN_AUTH_TYPE, wanted)

    """
    @param wanted
    """

    def with_wanted_remember_me(self, wanted=True):
        self.__is_wanted_remember_me = wanted
        return self

    def build(self):
        return {
            "wanted": list(self.__wanted_attributes.values()),
            "wanted_auth_types": [
                auth for (auth, b) in self.__wanted_auth_types.items() if b
            ],
            "wanted_remember_me": self.__is_wanted_remember_me,
        }

    def __is_number(self, num):
        return re.match(r"^\d+$", str(num)) is not None
