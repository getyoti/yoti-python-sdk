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

        super().__init__(data)
        self.__liveness_type = data.get("liveness_type", None)

    @property
    def liveness_type(self):
        """
        Returns the type of liveness resource.

        :return: liveness type
        :rtype: str or None
        """
        return self.__liveness_type

    def to_zoom_liveness_resource(self):
        """
        Converts this resource to a ZoomLivenessResourceResponse if applicable.

        :return: ZoomLivenessResourceResponse or None
        """
        if self.liveness_type == "zoom":
            return ZoomLivenessResourceResponse(self._data)
        return None

    def to_static_liveness_resource(self):
        """
        Converts this resource to a StaticLivenessResourceResponse if applicable.

        :return: StaticLivenessResourceResponse or None
        """
        if self.liveness_type == "static":
            return StaticLivenessResourceResponse(self._data)
        return None

    @staticmethod
    def filter_resources(resources, resource_type):
        """
        Filters and converts resources to the specified type.

        :param resources: List of raw resources
        :type resources: list[dict]
        :param resource_type: The target resource type ('zoom' or 'static')
        :type resource_type: str
        :return: List of resources converted to the specified type
        :rtype: list[ZoomLivenessResourceResponse or StaticLivenessResourceResponse]
        """
        filtered_resources = []
        for resource in resources:
            resource_obj = LivenessResourceResponse(resource)
            if resource_type == "zoom":
                zoom_resource = resource_obj.to_zoom_liveness_resource()
                if zoom_resource:
                    filtered_resources.append(zoom_resource)
            elif resource_type == "static":
                static_resource = resource_obj.to_static_liveness_resource()
                if static_resource:
                    filtered_resources.append(static_resource)
        return filtered_resources

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

        self.__image = FrameResponse(data["image"]) if "image" in data.keys() else None

    @property
    def image(self):
        """
        Returns the associated image for the static liveness resource.

        :return: the image
        :rtype: MediaResponse or None
        """
        return self.__image

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
