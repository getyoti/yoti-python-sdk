from .media_response import MediaResponse
from .resource_response import ResourceResponse


class FaceCaptureResponse(ResourceResponse):
    """
    Represents a Face Capture resource for a given session
    """

    def __init__(self, data=None):
        self._data = data or {}
        ResourceResponse.__init__(self, data)

    @property
    def id(self):
        return self._data.get("id")

    @property
    def source(self):
        return self._data.get("source")

    @property
    def image(self):
        return MediaResponse(data=self._data.get("image") or {})

    @property
    def tasks(self):
        return self._data.get("tasks") or []
