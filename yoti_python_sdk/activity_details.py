# -*- coding: utf-8 -*-
import json

import collections

from yoti_python_sdk import config
from yoti_python_sdk.protobuf.v1.protobuf import Protobuf


class ActivityDetails:
    def __init__(self, receipt, decrypted_profile=None):
        self.decrypted_profile = decrypted_profile
        self.user_profile = {}
        self.base64_selfie_uri = None

        if decrypted_profile and hasattr(decrypted_profile, 'attributes'):
            for field in decrypted_profile.attributes:
                value = Protobuf().value_based_on_content_type(
                    field.value,
                    field.content_type
                )
                self.user_profile[field.name] = value

                if field.name == 'selfie':
                    self.try_parse_selfie_field(field)

                if field.name.startswith(config.ATTRIBUTE_AGE_OVER) or field.name.startswith(
                        config.ATTRIBUTE_AGE_UNDER):
                    self.try_parse_age_verified_field(field)

                if field.name == config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS:
                    self.try_convert_structured_postal_address_to_dict(field)

            self.set_address_to_be_formatted_address_if_null()

        self.user_id = receipt['remember_me_id']
        self.outcome = receipt['sharing_outcome']

    def try_parse_selfie_field(self, field):
        self.base64_selfie_uri = Protobuf().image_uri_based_on_content_type(
            field.value,
            field.content_type
        )

    def try_parse_age_verified_field(self, field):
        if field is not None:
            is_age_verified = Protobuf().value_based_on_content_type(
                field.value,
                field.content_type
            )
            if is_age_verified == 'true':
                self.user_profile['is_age_verified'] = True
                return
            if is_age_verified == 'false':
                self.user_profile['is_age_verified'] = False
                return

        raise TypeError("age_verified_field unable to be parsed")

    def try_convert_structured_postal_address_to_dict(self, field):
        decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict)
        self.user_profile[config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS] = decoder.decode(field.value)

    def set_address_to_be_formatted_address_if_null(self):
        if 'postal_address' not in self.user_profile and 'structured_postal_address' in self.user_profile:
            if 'formatted_address' in self.user_profile['structured_postal_address']:
                self.user_profile['postal_address'] = self.user_profile['structured_postal_address'][
                    'formatted_address']

    def __iter__(self):
        yield 'user_id', self.user_id
        yield 'outcome', self.outcome
        yield 'user_profile', self.user_profile
        yield 'base64_selfie_uri', self.base64_selfie_uri
