# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.doc_scan.constants import CAMERA
from yoti_python_sdk.doc_scan.constants import CAMERA_AND_UPLOAD
from yoti_python_sdk.utils import YotiSerializable, remove_null_values


class SdkConfig(YotiSerializable):
    """
    Provides configuration properties for the web/native clients
    """

    def __init__(
        self,
        allowed_capture_methods,
        primary_colour,
        secondary_colour,
        font_colour,
        locale,
        preset_issuing_country,
        success_url,
        error_url,
    ):
        """
        :param allowed_capture_methods: the allowed capture methods
        :type allowed_capture_methods: str
        :param primary_colour: the primary colour
        :type primary_colour: str
        :param secondary_colour: the secondary colour
        :type secondary_colour: str
        :param font_colour: the font colour
        :type font_colour: str
        :param locale: the locale
        :type locale: str
        :param preset_issuing_country: the preset issuing country
        :type preset_issuing_country: str
        :param success_url: the success url
        :type success_url: str
        :param error_url: the error url
        :type error_url: str
        """
        self.__allowed_capture_methods = allowed_capture_methods
        self.__primary_colour = primary_colour
        self.__secondary_colour = secondary_colour
        self.__font_colour = font_colour
        self.__locale = locale
        self.__preset_issuing_country = preset_issuing_country
        self.__success_url = success_url
        self.__error_url = error_url

    @property
    def allowed_capture_methods(self):
        """
        The methods allowed for capturing document images

        :return: the allowed capture methods
        """
        return self.__allowed_capture_methods

    @property
    def primary_colour(self):
        """
        The primary colour

        :return: the primary colour
        """
        return self.__primary_colour

    @property
    def secondary_colour(self):
        """
        The secondary colour

        :return: the secondary colour
        """
        return self.__secondary_colour

    @property
    def font_colour(self):
        """
        The font colour

        :return: the font colour
        """
        return self.__font_colour

    @property
    def locale(self):
        """
        The locale

        :return: the locale
        """
        return self.__locale

    @property
    def preset_issuing_country(self):
        """
        The preset issuing country

        :return: the preset issuing country
        """
        return self.__preset_issuing_country

    @property
    def success_url(self):
        """
        The success URL

        :return: the success url
        """
        return self.__success_url

    @property
    def error_url(self):
        """
        The error URL

        :return: the error url
        """
        return self.__error_url

    def to_json(self):
        return remove_null_values(
            {
                "allowed_capture_methods": self.allowed_capture_methods,
                "primary_colour": self.primary_colour,
                "secondary_colour": self.secondary_colour,
                "font_colour": self.font_colour,
                "locale": self.locale,
                "preset_issuing_country": self.preset_issuing_country,
                "success_url": self.success_url,
                "error_url": self.error_url,
            }
        )


class SdkConfigBuilder(object):
    """
    Builder to assist in the creation of :class:`SdkConfig`
    """

    def __init__(self):
        self.__allowed_capture_methods = None
        self.__primary_colour = None
        self.__secondary_colour = None
        self.__font_colour = None
        self.__locale = None
        self.__preset_issuing_country = None
        self.__success_url = None
        self.__error_url = None

    def with_allowed_capture_methods(self, allowed_capture_methods):
        """
        Sets the allowed capture methods on the builder

        :param allowed_capture_methods: the allowed capture methods
        :type allowed_capture_methods: str
        :return: the builder
        :rtype: SdkConfigBuilder
        """
        self.__allowed_capture_methods = allowed_capture_methods
        return self

    def with_allows_camera(self):
        """
        Sets the allowed capture method to "CAMERA"

        :return: the builder
        :rtype: SdkConfigBuilder
        """
        return self.with_allowed_capture_methods(CAMERA)

    def with_allows_camera_and_upload(self):
        """
        Sets the allowed capture method to "CAMERA_AND_UPLOAD"

        :return: the builder
        :rtype: SdkConfigBuilder
        """
        return self.with_allowed_capture_methods(CAMERA_AND_UPLOAD)

    def with_primary_colour(self, colour):
        """
        Sets the primary colour to be used by the web/native client

        :param colour: the primary colour, hexadecimal value e.g. #ff0000
        :type colour: str
        :return: the builder
        :rtype: SdkConfigBuilder
        """
        self.__primary_colour = colour
        return self

    def with_secondary_colour(self, colour):
        """
        Sets the secondary colour to be used by the web/native client (used on the button)

        :param colour: the secondary colour, hexadecimal value e.g. #ff0000
        :type colour: str
        :return: the builder
        :rtype: SdkConfigBuilder
        """
        self.__secondary_colour = colour
        return self

    def with_font_colour(self, colour):
        """
        Sets the font colour to be used by the web/native client (used on the button)

        :param colour: the font colour, hexadecimal value e.g. #ff0000
        :type colour: str
        :return: the builder
        :rtype: SdkConfigBuilder
        """
        self.__font_colour = colour
        return self

    def with_locale(self, locale):
        """
        Sets the language locale use by the web/native client

        :param locale: the locale, e.g. "en"
        :type locale: str
        :return: the builder
        :rtype: SdkConfigBuilder
        """
        self.__locale = locale
        return self

    def with_preset_issuing_country(self, country):
        """
        Sets the preset issuing country used by the web/native client

        :param country: the preset issuing country
        :type country: str
        :return: the builder
        :rtype: SdkConfigBuilder
        """
        self.__preset_issuing_country = country
        return self

    def with_success_url(self, url):
        """
        Sets the success URL for the redirect that follows the web/native client uploading documents successfully

        :param url: the success URL
        :type url: str
        :return: the builder
        :rtype: SdkConfigBuilder
        """
        self.__success_url = url
        return self

    def with_error_url(self, url):
        """
        Sets the error URL for the redirect that follows the web/native client uploading documents unsuccessfully

        :param url: the error URL
        :type url: str
        :return: the builder
        :rtype: SdkConfigBuilder
        """
        self.__error_url = url
        return self

    def build(self):
        return SdkConfig(
            self.__allowed_capture_methods,
            self.__primary_colour,
            self.__secondary_colour,
            self.__font_colour,
            self.__locale,
            self.__preset_issuing_country,
            self.__success_url,
            self.__error_url,
        )
