# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.doc_scan.session.retrieve.media_response import MediaResponse


class FileResponse(object):
    """
    Represents a file
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
        Returns the media associated with the file

        :return: the media
        :rtype: MediaResponse or None
        """
        return self.__media
