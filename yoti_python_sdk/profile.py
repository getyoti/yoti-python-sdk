# -*- coding: utf-8 -*-
import logging

from yoti_python_sdk import attribute_parser, config, multivalue, document_details
from yoti_python_sdk.anchor import Anchor
from yoti_python_sdk.attribute import Attribute
from yoti_python_sdk.image import Image
from yoti_python_sdk.age_verification import AgeVerification


class BaseProfile(object):
    def __init__(self, profile_attributes):
        self.attributes = {}
        self.verifications = None

        if profile_attributes:
            for field in profile_attributes:
                try:
                    value = attribute_parser.value_based_on_content_type(
                        field.value, field.content_type
                    )

                    # this will be removed in v3.0.0, so selfie also returns an Image object
                    if field.content_type in Image.allowed_types():
                        if field.name == config.ATTRIBUTE_SELFIE:
                            value = field.value

                    if field.name == config.ATTRIBUTE_DOCUMENT_IMAGES:
                        value = multivalue.filter_values(value, Image)
                    if field.name == config.ATTRIBUTE_DOCUMENT_DETAILS:
                        value = document_details.DocumentDetails(value)

                    anchors = Anchor().parse_anchors(field.anchors)

                    self.attributes[field.name] = Attribute(field.name, value, anchors)

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

    def get_attribute(self, attribute_name):
        """
        retrieves an attribute based on its name
        :param attribute_name:
        :return: Attribute
        """
        if attribute_name in self.attributes:
            return self.attributes.get(attribute_name)
        else:
            return None


class Profile(BaseProfile):
    def __init__(self, profile_attributes):
        super(Profile, self).__init__(profile_attributes)
        self.ensure_postal_address()

    @property
    def date_of_birth(self):
        """date_of_birth represents the user's date of birth as a string.
        Will be changed to return a datetime in v3.0.0.
        Will be None if not provided by Yoti.
        :return: Attribute(str)
        """
        return self.get_attribute(config.ATTRIBUTE_DATE_OF_BIRTH)

    @property
    def family_name(self):
        """family_name represents the user's family name. This will be None if not provided by Yoti.
        :return: Attribute(str)
        """
        return self.get_attribute(config.ATTRIBUTE_FAMILY_NAME)

    @property
    def given_names(self):
        """given_names represents the user's given names. This will be None if not provided by Yoti.
        :return: Attribute(str)
        """
        return self.get_attribute(config.ATTRIBUTE_GIVEN_NAMES)

    @property
    def full_name(self):
        """full_name represents the user's full name.
        If family_name and given_names are present, the value will be equal to the string 'given_names + " " + family_name'.
        Will be None if not provided by Yoti.
        :return: Attribute(str)
        """
        return self.get_attribute(config.ATTRIBUTE_FULL_NAME)

    @property
    def gender(self):
        """gender corresponds to the gender in the registered document.
        The value will be one of the strings "MALE", "FEMALE", "TRANSGENDER" or "OTHER".
        Will be None if not provided by Yoti.
        :return: Attribute(str)
        """
        return self.get_attribute(config.ATTRIBUTE_GENDER)

    @property
    def nationality(self):
        """nationality corresponds to the nationality in the passport.
        The value is an ISO-3166-1 alpha-3 code with ICAO9303 (passport) extensions.
        Will be None if not provided by Yoti.
        :return: Attribute(str)
        """
        return self.get_attribute(config.ATTRIBUTE_NATIONALITY)

    @property
    def email_address(self):
        """email_address represents the user's email address. This will be None if not provided by Yoti.
        :return: Attribute(str)
        """
        return self.get_attribute(config.ATTRIBUTE_EMAIL_ADDRESS)

    @property
    def phone_number(self):
        """phone_number represents the user's mobile phone number. This will be None if not provided by Yoti.
        :return: Attribute(str)
        """
        return self.get_attribute(config.ATTRIBUTE_PHONE_NUMBER)

    @property
    def postal_address(self):
        """postal_address represents the user's address. This will be None if not provided by Yoti.
        :return: Attribute(str)
        """
        return self.get_attribute(config.ATTRIBUTE_POSTAL_ADDRESS)

    @property
    def selfie(self):
        """selfie is a photograph of the user. Will be None if not provided by Yoti.
        :return: Attribute(image)
        """
        return self.get_attribute(config.ATTRIBUTE_SELFIE)

    @property
    def structured_postal_address(self):
        """structured_postal_address represents the user's address represented as an OrderedDict.
        This will be None if not provided by Yoti.
        :return: Attribute(OrderedDict)
        """
        return self.get_attribute(config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS)

    @property
    def document_images(self):
        """document_images returns a tuple of document images cropped from the image in the capture page.
        There can be multiple images as per the number of regions in the capture in this attribute.
        Will be None if not provided by Yoti.
        :return: Attribute(tuple(image))
        """
        return self.get_attribute(config.ATTRIBUTE_DOCUMENT_IMAGES)

    @property
    def document_details(self):
        return self.get_attribute(config.ATTRIBUTE_DOCUMENT_DETAILS)

    def get_age_verifications(self):
        self.__find_all_age_verifications()
        return [self.verifications[key] for key in self.verifications.keys()]

    def find_age_over_verification(self, age):
        self.__find_all_age_verifications()
        if config.ATTRIBUTE_AGE_OVER + str(age) in self.verifications:
            return self.verifications[config.ATTRIBUTE_AGE_OVER + str(age)]
        return None

    def find_age_under_verification(self, age):
        self.__find_all_age_verifications()
        if (config.ATTRIBUTE_AGE_UNDER + str(age)) in self.verifications:
            return self.verifications[config.ATTRIBUTE_AGE_UNDER + str(age)]
        return None

    def __find_all_age_verifications(self):
        if self.verifications is None:
            self.verifications = {}
            for key in self.attributes:
                attribute = self.attributes[key]
                if hasattr(
                    attribute, "name"
                ):  # This will be changed in v3 as selfie will be an object rather than a string
                    if (
                        config.ATTRIBUTE_AGE_OVER in attribute.name
                        or config.ATTRIBUTE_AGE_UNDER in attribute.name
                    ):
                        self.verifications[attribute.name] = AgeVerification(attribute)

    def ensure_postal_address(self):
        if (
            config.ATTRIBUTE_POSTAL_ADDRESS not in self.attributes
            and config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS in self.attributes
        ):
            structured_postal_address = self.attributes[
                config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS
            ]

            if config.KEY_FORMATTED_ADDRESS in structured_postal_address.value:
                formatted_address = structured_postal_address.value[
                    config.KEY_FORMATTED_ADDRESS
                ]
                self.attributes[config.ATTRIBUTE_POSTAL_ADDRESS] = Attribute(
                    config.ATTRIBUTE_POSTAL_ADDRESS,
                    formatted_address,
                    structured_postal_address.anchors,
                )


class ApplicationProfile(BaseProfile):
    def __init__(self, profile_attributes):
        super(ApplicationProfile, self).__init__(profile_attributes)

    @property
    def application_name(self):
        """
        application_name is the name of the application set in Yoti Hub
        :return: Attribute(str)
        """
        return self.get_attribute(config.ATTRIBUTE_APPLICATION_NAME)

    @property
    def application_url(self):
        """
        application_url is the url of the application set in Yoti Hub
        :return: Attribute(str)
        """
        return self.get_attribute(config.ATTRIBUTE_APPLICATION_URL)

    @property
    def application_logo(self):
        """
        application_logo is the Image of the application logo set in Yoti Hub
        :return: Attribute(str)
        """
        return self.get_attribute(config.ATTRIBUTE_APPLICATION_LOGO)

    @property
    def application_receipt_bg_color(self):
        """
        application_receipt_bg_color is the background color of the application set in Yoti Hub
        :return: Attribute(str)
        """
        return self.get_attribute(config.ATTRIBUTE_APPLICATION_RECEIPT_BGCOLOR)
