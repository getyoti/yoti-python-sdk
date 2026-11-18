# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .media_response import MediaResponse


class ImageResponse(object):
    """
    Represents an image resource within a static liveness check
    """

    def __init__(self, data=None):
        """
        :param data: the data to parse
        :type data: dict or None
        """
        if data is None:
            data = dict()

        self.__media = (
            MediaResponse(data["media"]) if "media" in data.keys() else None
        )

    @property
    def media(self):
        """
        Returns the media information for the image

        :return: the media
        :rtype: MediaResponse or None
        """
        return self.__media
