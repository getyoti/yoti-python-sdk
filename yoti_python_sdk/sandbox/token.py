from yoti_python_sdk.sandbox.attribute import SandboxAttribute
from yoti_python_sdk import config
import base64


class YotiTokenResponse(object):
    def __init__(self, token):
        self.__token = token

    @property
    def token(self):
        """
        The token to be used by the Client

        :return: the token
        """
        return self.__token


class YotiTokenRequest(object):
    def __init__(self, remember_me_id=None, sandbox_attributes=None):
        if remember_me_id is None:
            remember_me_id = ""

        if sandbox_attributes is None:
            sandbox_attributes = []

        self.remember_me_id = remember_me_id
        self.sandbox_attributes = sandbox_attributes

    def __dict__(self):
        return {
            "remember_me_id": self.remember_me_id,
            "profile_attributes": self.sandbox_attributes,
        }

    @staticmethod
    def builder():
        """
        Creates an instance of the yoti token request builder

        :return: instance of YotiTokenRequestBuilder
        """
        return YotiTokenRequestBuilder()


class YotiTokenRequestBuilder(object):
    def __init__(self):
        self.remember_me_id = None
        self.attributes = []

    def with_remember_me_id(self, remember_me_id):
        """
        Sets the remember me id on the builder

        :param remember_me_id: the remember me id
        :return: the updated builder
        """
        self.remember_me_id = remember_me_id
        return self

    def with_attribute(self, sandbox_attribute):
        """
        Appends a SandboxAttribute to the list of attributes on the builder

        :param SandboxAttribute sandbox_attribute:
        :return: the updated builder
        """
        self.attributes.append(sandbox_attribute)
        return self

    def with_given_names(self, value, anchors=None):
        """
        Creates and appends a SandboxAttribute for given names

        :param str value: the value
        :param list[SandboxAnchor] anchors: optional list of anchors
        :return:
        """
        attribute = self.__create_attribute(
            config.ATTRIBUTE_GIVEN_NAMES, value, anchors
        )
        return self.with_attribute(attribute)

    def with_family_name(self, value, anchors=None):
        """
        Creates and appends a SandboxAttribute for family name

        :param str value: the value
        :param list[SandboxAnchor] anchors: optional list of anchors
        :return:
        """
        attribute = self.__create_attribute(
            config.ATTRIBUTE_FAMILY_NAME, value, anchors
        )
        return self.with_attribute(attribute)

    def with_full_name(self, value, anchors=None):
        """
        Creates and appends a SandboxAttribute for full name

        :param str value: the value
        :param list[SandboxAnchor] anchors: optional list of anchors
        :return:
        """
        attribute = self.__create_attribute(config.ATTRIBUTE_FULL_NAME, value, anchors)
        return self.with_attribute(attribute)

    def with_date_of_birth(self, value, anchors=None):
        """
        Creates and appends a SandboxAttribute for date of birth

        :param str value: the value
        :param list[SandboxAnchor] anchors: optional list of anchors
        :return:
        """
        attribute = self.__create_attribute(
            config.ATTRIBUTE_DATE_OF_BIRTH, value, anchors
        )
        return self.with_attribute(attribute)

    def with_age_verification(self, age_verification):
        """
        Creates and appends a SandboxAttribute with a given age verification

        :param SandboxAgeVerification age_verification: the age verification
        :return:
        """
        return self.with_attribute(age_verification.to_attribute())

    def with_gender(self, value, anchors=None):
        """
        Creates and appends a SandboxAttribute for gender

        :param str value: the value
        :param list[SandboxAnchor] anchors: optional list of anchors
        :return:
        """
        attribute = self.__create_attribute(config.ATTRIBUTE_GENDER, value, anchors)
        return self.with_attribute(attribute)

    def with_phone_number(self, value, anchors=None):
        """
        Creates and appends a SandboxAttribute for phone number

        :param str value: the value
        :param list[SandboxAnchor] anchors: optional list of anchors
        :return:
        """
        attribute = self.__create_attribute(
            config.ATTRIBUTE_PHONE_NUMBER, value, anchors
        )
        return self.with_attribute(attribute)

    def with_nationality(self, value, anchors=None):
        """
        Creates and appends a SandboxAttribute for nationality

        :param str value: the value
        :param list[SandboxAnchor] anchors: optional list of anchors
        :return:
        """
        attribute = self.__create_attribute(
            config.ATTRIBUTE_NATIONALITY, value, anchors
        )
        return self.with_attribute(attribute)

    def with_postal_address(self, value, anchors=None):
        """
        Creates and appends a SandboxAttribute for postal address

        :param str value: the value
        :param list[SandboxAnchor] anchors: optional list of anchors
        :return:
        """
        attribute = self.__create_attribute(
            config.ATTRIBUTE_POSTAL_ADDRESS, value, anchors
        )
        return self.with_attribute(attribute)

    def with_structured_postal_address(self, value, anchors=None):
        """
        Creates and appends a SandboxAttribute for structured postal address

        :param str value: the value
        :param list[SandboxAnchor] anchors: optional list of anchors
        :return:
        """
        attribute = self.__create_attribute(
            config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS, value, anchors
        )
        return self.with_attribute(attribute)

    def with_selfie(self, value, anchors=None):
        """
        Creates and appends a SandboxAttribute for a selfie

        :param str value: the value
        :param list[SandboxAnchor] anchors: optional list of anchors
        :return:
        """
        base64_selfie = base64.b64encode(value).decode("utf-8")
        return self.with_base64_selfie(base64_selfie, anchors)

    def with_base64_selfie(self, value, anchors=None):
        """
        Creates and appends a SandboxAttribute for given names

        :param str value: base64 encoded value
        :param list[SandboxAnchor] anchors: optional list of anchors
        :return:
        """
        attribute = self.__create_attribute(config.ATTRIBUTE_SELFIE, value, anchors)
        return self.with_attribute(attribute)

    def with_email_address(self, value, anchors=None):
        """
        Creates and appends a SandboxAttribute for email address

        :param str value: the value
        :param list[SandboxAnchor] anchors: optional list of anchors
        :return:
        """
        attribute = self.__create_attribute(
            config.ATTRIBUTE_EMAIL_ADDRESS, value, anchors
        )
        return self.with_attribute(attribute)

    def with_document_details(self, value, anchors=None):
        """
        Creates and appends a SandboxAttribute for document details

        :param str value: the value
        :param list[SandboxAnchor] anchors: optional list of anchors
        :return:
        """
        attribute = self.__create_attribute(
            config.ATTRIBUTE_DOCUMENT_DETAILS, value, anchors
        )
        return self.with_attribute(attribute)

    def build(self):
        """
        Creates an instance of YotiTokenRequest using the supplied values

        :return: instance of YotiTokenRequest
        """
        return YotiTokenRequest(self.remember_me_id, self.attributes)

    @staticmethod
    def __create_attribute(name, value, anchors=None):
        return SandboxAttribute(name, value, anchors)
