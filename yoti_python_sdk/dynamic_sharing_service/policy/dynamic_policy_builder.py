# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from yoti_python_sdk import config

from .wanted_attribute_builder import WantedAttributeBuilder


class DynamicPolicyBuilder(object):
    """
    Builder for DynamicPolicy
    """

    SELFIE_AUTH_TYPE = 1
    PIN_AUTH_TYPE = 2

    def __init__(self):
        self.__wanted_attributes = {}
        self.__wanted_auth_types = {}
        self.__is_wanted_remember_me = False

    def with_wanted_attribute(self, wanted_attribute):
        """
        @param wanted_attribute
        """
        key = (
            wanted_attribute["derivation"]
            if wanted_attribute.get("derivation", False)
            else wanted_attribute["name"]
        )
        self.__wanted_attributes[key] = wanted_attribute
        return self

    def __attribute_keyword_parser(self, attributeBuilder, **kwargs):
        constraints = kwargs.get("constraints", False)
        if constraints:
            attributeBuilder.with_constraint(constraints)

        accept_self_asserted = kwargs.get("accept_self_asserted", None)
        if accept_self_asserted is not None:
            attributeBuilder.with_accept_self_asserted(accept_self_asserted)

    def with_wanted_attribute_by_name(self, wanted_name, **kwargs):
        """
        @param wanted_name The name of the attribute to include
        """
        attributeBuilder = WantedAttributeBuilder().with_name(wanted_name)
        self.__attribute_keyword_parser(attributeBuilder, **kwargs)

        return self.with_wanted_attribute(attributeBuilder.build())

    def with_family_name(self, **kwargs):
        return self.with_wanted_attribute_by_name(
            config.ATTRIBUTE_FAMILY_NAME, **kwargs
        )

    def with_given_names(self, **kwargs):
        return self.with_wanted_attribute_by_name(
            config.ATTRIBUTE_GIVEN_NAMES, **kwargs
        )

    def with_full_name(self, **kwargs):
        return self.with_wanted_attribute_by_name(config.ATTRIBUTE_FULL_NAME, **kwargs)

    def with_date_of_birth(self, **kwargs):
        return self.with_wanted_attribute_by_name(
            config.ATTRIBUTE_DATE_OF_BIRTH, **kwargs
        )

    def with_age_derived_attribute(self, derivation, **kwargs):
        attributeBuilder = (
            WantedAttributeBuilder()
            .with_name(config.ATTRIBUTE_DATE_OF_BIRTH)
            .with_derivation(derivation)
        )
        self.__attribute_keyword_parser(attributeBuilder, **kwargs)
        return self.with_wanted_attribute(attributeBuilder.build())

    def with_age_over(self, age, **kwargs):
        assert self.__is_number(age)
        return self.with_age_derived_attribute(
            config.ATTRIBUTE_AGE_OVER + str(age), **kwargs
        )

    def with_age_under(self, age, **kwargs):
        assert self.__is_number(age)
        return self.with_age_derived_attribute(
            config.ATTRIBUTE_AGE_UNDER + str(age), **kwargs
        )

    def with_gender(self, **kwargs):
        return self.with_wanted_attribute_by_name(config.ATTRIBUTE_GENDER, **kwargs)

    def with_postal_address(self, **kwargs):
        return self.with_wanted_attribute_by_name(
            config.ATTRIBUTE_POSTAL_ADDRESS, **kwargs
        )

    def with_structured_postal_address(self, **kwargs):
        return self.with_wanted_attribute_by_name(
            config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS, **kwargs
        )

    def with_nationality(self, **kwargs):
        return self.with_wanted_attribute_by_name(
            config.ATTRIBUTE_NATIONALITY, **kwargs
        )

    def with_phone_number(self, **kwargs):
        return self.with_wanted_attribute_by_name(
            config.ATTRIBUTE_PHONE_NUMBER, **kwargs
        )

    def with_selfie(self, **kwargs):
        return self.with_wanted_attribute_by_name(config.ATTRIBUTE_SELFIE, **kwargs)

    def with_email(self, **kwargs):
        return self.with_wanted_attribute_by_name(
            config.ATTRIBUTE_EMAIL_ADDRESS, **kwargs
        )

    def with_document_details(self, **kwargs):
        return self.with_wanted_attribute_by_name(
            config.ATTRIBUTE_DOCUMENT_DETAILS, **kwargs
        )

    def with_document_images(self, **kwargs):
        return self.with_wanted_attribute_by_name(
            config.ATTRIBUTE_DOCUMENT_IMAGES, **kwargs
        )

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
