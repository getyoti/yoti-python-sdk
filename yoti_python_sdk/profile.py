# -*- coding: utf-8 -*-
import logging

from yoti_python_sdk import attribute_parser, config, multivalue
from yoti_python_sdk.anchor import Anchor
from yoti_python_sdk.attribute import Attribute
from yoti_python_sdk.image import Image


class Profile:
    def __init__(self, profile_attributes):
        self.attributes = {}

        if profile_attributes:
            for field in profile_attributes:
                try:
                    value = attribute_parser.value_based_on_content_type(
                        field.value,
                        field.content_type
                    )

                    # this will be removed in v3.0.0, so selfie also returns an Image object
                    if field.content_type in Image.allowed_types():
                        if field.name == config.ATTRIBUTE_SELFIE:
                            value = field.value

                    if field.name == config.ATTRIBUTE_DOCUMENT_IMAGES:
                        value = multivalue.filter_values(value, Image)

                    anchors = Anchor().parse_anchors(field.anchors)

                    self.attributes[field.name] = Attribute(field.name, value, anchors)

                except ValueError as ve:
                    if logging.getLogger().propagate:
                        logging.warning(ve)
                except Exception as exc:
                    if logging.getLogger().propagate:
                        logging.warning(
                            'Error parsing profile attribute:{0}, exception: {1} - {2}'.format(field.name, type(exc).__name__, exc))

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

    @property
    def document_images(self):
        return self.get_attribute(config.ATTRIBUTE_DOCUMENT_IMAGES)

    def get_attribute(self, attribute_name):
        if attribute_name in self.attributes:
            return self.attributes.get(attribute_name)
        else:
            return None

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
