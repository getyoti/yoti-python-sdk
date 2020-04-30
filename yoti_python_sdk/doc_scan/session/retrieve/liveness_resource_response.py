# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .resource_response import ResourceResponse
from .face_map_response import FaceMapResponse
from .frame_response import FrameResponse


class LivenessResourceResponse(ResourceResponse):
    """
    Represents a Liveness resource for a given session
    """

    def __init__(self, data=None):
        if data is None:
            data = dict()

        ResourceResponse.__init__(self, data)

        self.__liveness_type = data.get("liveness_type", None)

    @property
    def liveness_type(self):
        return self.__liveness_type


class ZoomLivenessResourceResponse(LivenessResourceResponse):
    """
    Represents a Zoom Liveness resource for a given session
    """

    def __init__(self, data=None):
        """
        :param data: the data to parse
        :type data: dict or None
        """
        if data is None:
            data = dict()

        LivenessResourceResponse.__init__(self, data)

        self.__facemap = (
            FaceMapResponse(data["facemap"]) if "facemap" in data.keys() else None
        )
        self.__frames = [FrameResponse(frame) for frame in data.get("frames", [])]

    @property
    def facemap(self):
        """
        Returns the associated facemap information for
        the zoom liveness resource

        :return: the facemap
        :rtype: FaceMapResponse or None
        """
        return self.__facemap

    @property
    def frames(self):
        """
        Returns the list of associated frames for
        the zoom liveness resource

        :return: the frames
        :rtype: list[FrameResponse]
        """
        return self.__frames
