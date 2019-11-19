# -*- coding: utf-8 -*-
import collections
import json
import logging
from deprecated import deprecated
from datetime import datetime

from yoti_python_sdk import attribute_parser, config
from yoti_python_sdk.profile import Profile, ApplicationProfile
from yoti_python_sdk.share.extra_data import ExtraData


class ActivityDetails:
    def __init__(
        self,
        receipt,
        decrypted_profile=None,
        decrypted_application_profile=None,
        decrypted_extra_data=None,
    ):
        self.decrypted_profile = decrypted_profile
        self.user_profile = {}  # will be removed in v3.0.0
        self.base64_selfie_uri = None
        self.decrypted_application_profile = decrypted_application_profile
        self.extra_data = None

        if decrypted_profile and hasattr(decrypted_profile, "attributes"):
            decrypted_profile_attributes = decrypted_profile.attributes
            self.profile = Profile(decrypted_profile_attributes)

            for field in decrypted_profile_attributes:  # will be removed in v3.0.0
                try:
                    value = attribute_parser.value_based_on_content_type(
                        field.value, field.content_type
                    )

                    if field.name == config.ATTRIBUTE_SELFIE:
                        self.base64_selfie_uri = value.base64_content()
                        value = (
                            field.value
                        )  # set value to be byte content, for backwards compatibility

                    if field.name == config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS:
                        value = self.try_convert_structured_postal_address_to_dict(
                            field
                        )

                    if field.name.startswith(
                        config.ATTRIBUTE_AGE_OVER
                    ) or field.name.startswith(config.ATTRIBUTE_AGE_UNDER):
                        self.try_parse_age_verified_field(field)

                    self.user_profile[field.name] = value

                except ValueError as ve:
                    if logging.getLogger().propagate:
                        logging.warning(ve)
                except Exception as exc:
                    if logging.getLogger().propagate:
                        logging.warning(
                            "Error parsing profile attribute:{0}, exception: {1} - {2}".format(
                                field.name, type(exc).__name__, exc
                            )
                        )

            self.ensure_postal_address()

        if decrypted_application_profile and hasattr(
            decrypted_application_profile, "attributes"
        ):
            decrypted_application_profile_attributes = (
                decrypted_application_profile.attributes
            )
            self.application_profile = ApplicationProfile(
                decrypted_application_profile_attributes
            )

        self.__remember_me_id = receipt.get("remember_me_id")
        self.parent_remember_me_id = receipt.get("parent_remember_me_id")
        self.outcome = receipt.get("sharing_outcome")
        self.receipt_id = receipt.get("receipt_id")
        self.extra_data = receipt.get("extra_data")
        timestamp = receipt.get("timestamp")

        if timestamp is not None:
            self.timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")

        if decrypted_extra_data:
            self.extra_data = ExtraData(decrypted_extra_data)

    @property
    def remember_me_id(self):
        return self.__remember_me_id

    @property
    @deprecated
    def user_id(self):
        return self.__remember_me_id

    @user_id.setter
    @deprecated
    def user_id(self, value):
        self.__remember_me_id = value

    @deprecated
    def try_parse_age_verified_field(self, field):
        if field is not None:
            age_verified = attribute_parser.value_based_on_content_type(
                field.value, field.content_type
            )
            if age_verified == "true":
                self.user_profile[config.KEY_AGE_VERIFIED] = True
                return
            if age_verified == "false":
                self.user_profile[config.KEY_AGE_VERIFIED] = False
                return

            print(
                "age_verified_field value: '{0}' was unable to be parsed into a boolean value".format(
                    age_verified
                )
            )

    @staticmethod
    def try_convert_structured_postal_address_to_dict(field):
        decoder = json.JSONDecoder(
            object_pairs_hook=collections.OrderedDict, strict=False
        )
        value_to_decode = field.value
        if not isinstance(value_to_decode, str):
            value_to_decode = value_to_decode.decode()

        return decoder.decode(value_to_decode)

    def ensure_postal_address(self):
        # setting in 'user_profile'  - will be removed once user_profile is removed
        if (
            config.ATTRIBUTE_POSTAL_ADDRESS not in self.user_profile
            and config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS in self.user_profile
        ):
            if (
                config.KEY_FORMATTED_ADDRESS
                in self.user_profile[config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS]
            ):
                self.user_profile[config.ATTRIBUTE_POSTAL_ADDRESS] = self.user_profile[
                    config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS
                ][config.KEY_FORMATTED_ADDRESS]

    def __iter__(self):
        yield "user_id", self.__remember_me_id  # Using the private member directly to avoid a deprecation warning
        yield "parent_remember_me_id", self.parent_remember_me_id
        yield "outcome", self.outcome
        yield "receipt_id", self.receipt_id
        yield "user_profile", self.user_profile
        yield "profile", self.profile
        yield "base64_selfie_uri", self.base64_selfie_uri
        yield "remember_me_id", self.remember_me_id
