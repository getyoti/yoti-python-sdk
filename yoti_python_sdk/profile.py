# -*- coding: utf-8 -*-
import collections
import json

from yoti_python_sdk import config
from yoti_python_sdk.anchor import Anchor
from yoti_python_sdk.attribute import Attribute
from yoti_python_sdk.protobuf.v1.protobuf import Protobuf


class Profile:
    def __init__(self, profile_attributes):
        self.attributes = {}

        if profile_attributes:
            for field in profile_attributes:
                value = Protobuf().value_based_on_content_type(
                    field.value,
                    field.content_type
                )

                anchors = Anchor().parse_anchors(field.anchors)

                self.attributes[field.name] = Attribute(field.name, value, anchors)

                if field.name == config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS:
                    self.try_convert_structured_postal_address_to_dict(field, anchors)

            self.ensure_postal_address()

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
    def nationality(self):
        return self.get_attribute(config.ATTRIBUTE_NATIONALITY)

    @property
    def email_address(self):
        return self.get_attribute(config.ATTRIBUTE_EMAIL_ADDRESS)

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
        if attribute_name in self.attributes:
            return self.attributes.get(attribute_name)
        else:
            return None

    def try_convert_structured_postal_address_to_dict(self, field, anchors):
        decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict, strict=False)
        value_to_decode = field.value.decode()

        self.attributes[config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS] = Attribute(
            config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS,
            decoder.decode(value_to_decode),
            anchors)

    def ensure_postal_address(self):
        if config.ATTRIBUTE_POSTAL_ADDRESS not in self.attributes and config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS in self.attributes:
            structured_postal_address = self.attributes[config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS]

            if config.KEY_FORMATTED_ADDRESS in structured_postal_address.value:
                formatted_address = structured_postal_address.value[
                    config.KEY_FORMATTED_ADDRESS]
                self.attributes[config.ATTRIBUTE_POSTAL_ADDRESS] = Attribute(
                    config.ATTRIBUTE_POSTAL_ADDRESS,
                    formatted_address,
                    structured_postal_address.anchors)
