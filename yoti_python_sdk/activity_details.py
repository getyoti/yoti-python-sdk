# -*- coding: utf-8 -*-
import collections
import json

from yoti_python_sdk import config
from yoti_python_sdk.profile import Profile
from yoti_python_sdk.protobuf.v1.protobuf import Protobuf


class ActivityDetails:
    def __init__(self, receipt, decrypted_profile=None):
        self.decrypted_profile = decrypted_profile
        self.user_profile = {}  # will be removed in v3.0.0
        self.base64_selfie_uri = None

        if decrypted_profile and hasattr(decrypted_profile, 'attributes'):
            decrypted_profile_attributes = decrypted_profile.attributes
            self.profile = Profile(decrypted_profile_attributes)

            for field in decrypted_profile_attributes:  # will be removed in v3.0.0
                value = Protobuf().value_based_on_content_type(
                    field.value,
                    field.content_type
                )

                self.user_profile[field.name] = value

                if field.name == config.ATTRIBUTE_SELFIE:
                    self.try_parse_selfie_field(field)

                if field.name.startswith(config.ATTRIBUTE_AGE_OVER) or field.name.startswith(
                        config.ATTRIBUTE_AGE_UNDER):
                    self.try_parse_age_verified_field(field)

                if field.name == config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS:
                    self.try_convert_structured_postal_address_to_dict(field)

            self.ensure_postal_address()

        self.user_id = receipt['remember_me_id']
        self.outcome = receipt['sharing_outcome']

    def try_parse_selfie_field(self, field):
        self.base64_selfie_uri = Protobuf().image_uri_based_on_content_type(
            field.value,
            field.content_type
        )

    def try_parse_age_verified_field(self, field):
        if field is not None:
            age_verified = Protobuf().value_based_on_content_type(
                field.value,
                field.content_type
            )
            if age_verified == 'true':
                self.user_profile[config.KEY_AGE_VERIFIED] = True
                return
            if age_verified == 'false':
                self.user_profile[config.KEY_AGE_VERIFIED] = False
                return

            print(
                "age_verified_field value: '{0}' was unable to be parsed into a boolean value".format(age_verified))

    def try_convert_structured_postal_address_to_dict(self, field):
        decoder = json.JSONDecoder(object_pairs_hook=collections.OrderedDict, strict=False)
        value_to_decode = field.value
        if not isinstance(value_to_decode, str):
            value_to_decode = value_to_decode.decode()

        self.user_profile[config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS] = decoder.decode(value_to_decode)

    def ensure_postal_address(self):
        # setting in 'user_profile'  - will be removed once user_profile is removed
        if config.ATTRIBUTE_POSTAL_ADDRESS not in self.user_profile and config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS in self.user_profile:
            if config.KEY_FORMATTED_ADDRESS in self.user_profile[config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS]:
                self.user_profile[config.ATTRIBUTE_POSTAL_ADDRESS] = \
                    self.user_profile[config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS][
                        config.KEY_FORMATTED_ADDRESS]

    def __iter__(self):
        yield 'user_id', self.user_id
        yield 'outcome', self.outcome
        yield 'user_profile', self.user_profile
        yield 'profile', self.profile
        yield 'base64_selfie_uri', self.base64_selfie_uri
