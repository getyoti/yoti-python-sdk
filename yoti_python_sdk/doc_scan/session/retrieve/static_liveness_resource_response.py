# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .liveness_resource_response import LivenessResourceResponse
from .image_response import ImageResponse


class StaticLivenessResourceResponse(LivenessResourceResponse):
    """
    Represents a Static Liveness resource for a given session
    """

    def __init__(self, data=None):
        """
        :param data: the data to parse
        :type data: dict or None
        """
        if data is None:
            data = dict()

        LivenessResourceResponse.__init__(self, data)

        self.__image = (
            ImageResponse(data["image"]) if "image" in data.keys() else None
        )

    @property
    def image(self):
        """
        Returns the associated image for the static liveness resource

        :return: the image
        :rtype: ImageResponse or None
        """
        return self.__image
