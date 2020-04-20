# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.doc_scan.session.retrieve.media_response import MediaResponse


class FaceMapResponse(object):
    """
    Represents a FaceMap response object
    """

    def __init__(self, data=None):
        """
        :param data: the data to parse
        :type data: dict or None
        """
        if data is None:
            data = dict()

        self.__media = MediaResponse(data["media"]) if "media" in data.keys() else None

    @property
    def media(self):
        """
        Returns the associated media of the FaceMap

        :return: the media
        :rtype: MediaResponse or None
        """
        return self.__media
