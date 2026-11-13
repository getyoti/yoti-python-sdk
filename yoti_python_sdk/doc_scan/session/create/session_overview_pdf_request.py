# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.utils import YotiSerializable, remove_null_values


class SessionOverviewPdfRequest(YotiSerializable):
    """
    Represents the request body for generating a session overview PDF.

    All flags are optional. A flag that was not explicitly set is omitted
    from the serialised JSON entirely — it is NOT sent as ``false`` or
    ``null``.  Validation of the values is deferred to the backend.
    """

    def __init__(
        self,
        include_images=None,
        include_extracted_text=None,
        include_device_tracking=None,
    ):
        """
        :param include_images: whether to include images in the PDF
        :type include_images: bool or None
        :param include_extracted_text: whether to include extracted text
        :type include_extracted_text: bool or None
        :param include_device_tracking: whether to include device tracking info
        :type include_device_tracking: bool or None
        """
        self.__include_images = include_images
        self.__include_extracted_text = include_extracted_text
        self.__include_device_tracking = include_device_tracking

    @property
    def include_images(self):
        """
        :rtype: bool or None
        """
        return self.__include_images

    @property
    def include_extracted_text(self):
        """
        :rtype: bool or None
        """
        return self.__include_extracted_text

    @property
    def include_device_tracking(self):
        """
        :rtype: bool or None
        """
        return self.__include_device_tracking

    def to_json(self):
        return remove_null_values(
            {
                "include_images": self.__include_images,
                "include_extracted_text": self.__include_extracted_text,
                "include_device_tracking": self.__include_device_tracking,
            }
        )


class SessionOverviewPdfRequestBuilder(object):
    """
    Builder to assist in the creation of :class:`SessionOverviewPdfRequest`.
    """

    def __init__(self):
        self.__include_images = None
        self.__include_extracted_text = None
        self.__include_device_tracking = None

    def with_include_images(self, include_images=True):
        """
        Sets whether images should be included in the PDF.

        :param include_images: flag value
        :type include_images: bool
        :return: the builder
        :rtype: SessionOverviewPdfRequestBuilder
        """
        self.__include_images = include_images
        return self

    def with_include_extracted_text(self, include_extracted_text=True):
        """
        Sets whether extracted text should be included in the PDF.

        :param include_extracted_text: flag value
        :type include_extracted_text: bool
        :return: the builder
        :rtype: SessionOverviewPdfRequestBuilder
        """
        self.__include_extracted_text = include_extracted_text
        return self

    def with_include_device_tracking(self, include_device_tracking=True):
        """
        Sets whether device tracking information should be included in the PDF.

        :param include_device_tracking: flag value
        :type include_device_tracking: bool
        :return: the builder
        :rtype: SessionOverviewPdfRequestBuilder
        """
        self.__include_device_tracking = include_device_tracking
        return self

    def build(self):
        """
        Builds the :class:`SessionOverviewPdfRequest`.

        :return: the built request
        :rtype: SessionOverviewPdfRequest
        """
        return SessionOverviewPdfRequest(
            include_images=self.__include_images,
            include_extracted_text=self.__include_extracted_text,
            include_device_tracking=self.__include_device_tracking,
        )
