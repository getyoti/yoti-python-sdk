# -*- coding: utf-8 -*-
from yoti_python_sdk import date_parser
from yoti_python_sdk.profile import Profile, ApplicationProfile


class ActivityDetails:
    def __init__(
        self, receipt, decrypted_profile=None, decrypted_application_profile=None
    ):
        self.decrypted_profile = decrypted_profile
        self.decrypted_application_profile = decrypted_application_profile

        self.profile = self.__attributes_to_profile(decrypted_profile, Profile)
        self.application_profile = self.__attributes_to_profile(
            decrypted_application_profile, ApplicationProfile
        )

        self.__remember_me_id = receipt.get("remember_me_id")
        self.parent_remember_me_id = receipt.get("parent_remember_me_id")
        self.outcome = receipt.get("sharing_outcome")
        self.receipt_id = receipt.get("receipt_id")
        timestamp = receipt.get("timestamp")

        if timestamp is not None:
            self.timestamp = date_parser.datetime_from_string(timestamp)

    @property
    def remember_me_id(self):
        return self.__remember_me_id

    @staticmethod
    def __attributes_to_profile(attribute_dict, cls_type):
        if attribute_dict and hasattr(attribute_dict, "attributes"):
            return cls_type(attribute_dict.attributes)
        return None

    def __iter__(self):
        yield "user_id", self.__remember_me_id  # Using the private member directly to avoid a deprecation warning
        yield "parent_remember_me_id", self.parent_remember_me_id
        yield "outcome", self.outcome
        yield "receipt_id", self.receipt_id
        yield "profile", self.profile
        yield "application_profile", self.application_profile
        yield "base64_selfie_uri", self.base64_selfie_uri
        yield "remember_me_id", self.remember_me_id
