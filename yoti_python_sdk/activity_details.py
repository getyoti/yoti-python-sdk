# -*- coding: utf-8 -*-
import collections
import json

from yoti_python_sdk import config, attribute
from yoti_python_sdk.anchor import Anchor
from yoti_python_sdk.protobuf.v1.protobuf import Protobuf


class ActivityDetails:
    def __init__(self, receipt, decrypted_profile=None):
        self.decrypted_profile = decrypted_profile
        self.user_profile = {}  # will be deprecated in v3.0.0
        self.profile = {}
        self.base64_selfie_uri = None

        if decrypted_profile and hasattr(decrypted_profile, 'attributes'):
            for field in decrypted_profile.attributes:
                value = Protobuf().value_based_on_content_type(
                    field.value,
                    field.content_type
                )

                anchors = Anchor().parse_anchors(field.anchors)

                self.profile[field.name] = attribute.attribute(field.name, value, anchors)
                self.user_profile[field.name] = value  # will be deprecated in v3.0.0

                if field.name == 'selfie':
                    self.try_parse_selfie_field(field)

                if field.name.startswith(config.ATTRIBUTE_AGE_OVER) or field.name.startswith(
                        config.ATTRIBUTE_AGE_UNDER):
                    self.try_parse_age_verified_field(field, anchors)

                if field.name == config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS:
                    self.try_convert_structured_postal_address_to_dict(field, anchors)

            self.set_address_to_be_formatted_address_if_null(anchors)

        self.user_id = receipt['remember_me_id']
        self.outcome = receipt['sharing_outcome']

    def try_parse_selfie_field(self, field):
        self.base64_selfie_uri = Protobuf().image_uri_based_on_content_type(
            field.value,
            field.content_type
        )

    def try_parse_age_verified_field(self, field, anchors):
        if field is not None:
            is_age_verified = Protobuf().value_based_on_content_type(
                field.value,
                field.content_type
            )
            if is_age_verified == 'true':
                self.user_profile['is_age_verified'] = True
                self.profile['is_age_verified'] = attribute.attribute(is_age_verified, True, anchors)
                return
            if is_age_verified == 'false':
                self.user_profile['is_age_verified'] = False
                self.profile['is_age_verified'] = attribute.attribute(is_age_verified, False, anchors)
                return

        raise TypeError("age_verified_field unable to be parsed")

    def try_convert_structured_postal_address_to_dict(self, field, anchors):
        decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict, strict=False)
        value_to_decode = field.value
        if not isinstance(value_to_decode, str):
            value_to_decode = value_to_decode.decode()

        self.user_profile[config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS] = decoder.decode(value_to_decode)
        self.profile[config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS] = attribute.attribute(
            config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS,
            decoder.decode(value_to_decode),
            anchors)

    def set_address_to_be_formatted_address_if_null(self, anchors):
        if config.ATTRIBUTE_POSTAL_ADDRESS not in self.user_profile and config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS in self.user_profile:
            if config.KEY_FORMATTED_ADDRESS in self.user_profile[config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS]:
                self.user_profile[config.ATTRIBUTE_POSTAL_ADDRESS] = \
                    self.user_profile[config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS][
                        config.KEY_FORMATTED_ADDRESS]

        if config.ATTRIBUTE_POSTAL_ADDRESS not in self.profile and config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS in self.profile:
            if config.KEY_FORMATTED_ADDRESS in self.profile[config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS].value:
                formatted_address = self.profile[config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS].value[
                    config.KEY_FORMATTED_ADDRESS]
                self.profile[config.ATTRIBUTE_POSTAL_ADDRESS] = attribute.attribute(
                    config.ATTRIBUTE_POSTAL_ADDRESS,
                    formatted_address,
                    anchors)

    def __iter__(self):
        yield 'user_id', self.user_id
        yield 'outcome', self.outcome
        yield 'user_profile', self.user_profile
        yield 'profile', self.profile
        yield 'base64_selfie_uri', self.base64_selfie_uri
