# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .media_response import MediaResponse
from .frame_response import FrameResponse


class PageResponse(object):
    """
    Represents information about an uploaded document Page
    """

    def __init__(self, data=None):
        """
        :param data: the data to parse
        :type data: dict or None
        """
        if data is None:
            data = dict()

        self.__capture_method = (
            data["capture_method"] if "capture_method" in data.keys() else None
        )
        self.__media = MediaResponse(data["media"]) if "media" in data.keys() else None
        self.__frames = [FrameResponse(frame) for frame in data.get("frames", [])]

    @property
    def capture_method(self):
        """
        The capture method that was used for the Page

        :return: the capture method
        :rtype: str or None
        """
        return self.__capture_method

    @property
    def media(self):
        """
        The media associated with the Page

        :return: the media
        :rtype: MediaResponse or None
        """
        return self.__media

    @property
    def frames(self):
        """
        Returns the list of associated frames

        :return: the frames
        :rtype: list[FrameResponse]
        """
        return self.__frames
