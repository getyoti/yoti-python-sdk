# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.doc_scan.session.retrieve.media_response import MediaResponse


class ShareCodeMediaResponse(object):
    """
    Wraps a MediaResponse inside a share code resource field
    """

    def __init__(self, data=None):
        """
        :param data: the data to parse
        :type data: dict or None
        """
        if data is None:
            data = dict()

        if "media" in data and data["media"] is not None:
            self.__media = MediaResponse(data["media"])
        else:
            self.__media = None

    @property
    def media(self):
        """
        The media object

        :return: the media
        :rtype: MediaResponse or None
        """
        return self.__media
