# -*- coding: utf-8 -*-
import collections
import json

from yoti_python_sdk import config
from yoti_python_sdk.anchor import Anchor
from yoti_python_sdk.attribute import Attribute
from yoti_python_sdk.protobuf.v1.protobuf import Protobuf


class Profile:
    def __init__(self, profile_attributes):
        self.profile = {}

        if profile_attributes:
            for field in profile_attributes:
                value = Protobuf().value_based_on_content_type(
                    field.value,
                    field.content_type
                )

                anchors = Anchor().parse_anchors(field.anchors)

                self.profile[field.name] = Attribute(field.name, value, anchors)
                # self.profile[field.name] = Attribute(field.name, field.value, anchors)

                if field.name.startswith(config.ATTRIBUTE_AGE_OVER) or field.name.startswith(
                        config.ATTRIBUTE_AGE_UNDER):
                    self.try_parse_age_verified_field(field, anchors)

                if field.name == config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS:
                    self.try_convert_structured_postal_address_to_dict(field, anchors)

            self.ensure_postal_address(anchors)

    @property
    def date_of_birth(self):
        return self.get_attribute(config.ATTRIBUTE_DATE_OF_BIRTH)

    @property
    def family_name(self):
        return self.get_attribute(config.ATTRIBUTE_FAMILY_NAME)

    @property
    def full_name(self):
        return self.get_attribute(config.ATTRIBUTE_FULL_NAME)

    @property
    def gender(self):
        return self.get_attribute(config.ATTRIBUTE_GENDER)

    @property
    def given_names(self):
        return self.get_attribute(config.ATTRIBUTE_GIVEN_NAMES)

    @property
    def is_age_verified(self):
        return self.get_attribute(config.ATTRIBUTE_IS_AGE_VERIFIED)

    @property
    def nationality(self):
        return self.get_attribute(config.ATTRIBUTE_NATIONALITY)

    @property
    def phone_number(self):
        return self.get_attribute(config.ATTRIBUTE_PHONE_NUMBER)

    @property
    def postal_address(self):
        return self.get_attribute(config.ATTRIBUTE_POSTAL_ADDRESS)

    @property
    def selfie(self):
        return self.get_attribute(config.ATTRIBUTE_SELFIE)

    @property
    def structured_postal_address(self):
        return self.get_attribute(config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS)

    def get_attribute(self, attribute_name):
        if attribute_name in self.profile:
            return self.profile.get(attribute_name)
        else:
            return None

    def try_parse_age_verified_field(self, field, anchors):
        if field is not None:
            is_age_verified = Protobuf().value_based_on_content_type(
                field.value,
                field.content_type
            )
            if is_age_verified == 'true':
                self.profile[config.ATTRIBUTE_IS_AGE_VERIFIED] = Attribute(is_age_verified, True, anchors)
                return
            if is_age_verified == 'false':
                self.profile[config.ATTRIBUTE_IS_AGE_VERIFIED] = Attribute(is_age_verified, False, anchors)
                return

        raise TypeError("age_verified_field unable to be parsed")

    def try_convert_structured_postal_address_to_dict(self, field, anchors):
        decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict, strict=False)
        value_to_decode = field.value
        if not isinstance(value_to_decode, str):
            value_to_decode = value_to_decode.decode()

        self.profile[config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS] = Attribute(
            config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS,
            decoder.decode(value_to_decode),
            anchors)

    def ensure_postal_address(self, anchors):
        if config.ATTRIBUTE_POSTAL_ADDRESS not in self.profile and config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS in self.profile:
            if config.KEY_FORMATTED_ADDRESS in self.profile[config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS].value:
                formatted_address = self.profile[config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS].value[
                    config.KEY_FORMATTED_ADDRESS]
                self.profile[config.ATTRIBUTE_POSTAL_ADDRESS] = Attribute(
                    config.ATTRIBUTE_POSTAL_ADDRESS,
                    formatted_address,
                    anchors)
