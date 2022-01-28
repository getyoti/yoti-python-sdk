from .media_response import MediaResponse
from .resource_response import ResourceResponse


class FaceCaptureResponse(ResourceResponse):
    """
    Represents a Face Capture resource for a given session.
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


class FaceCaptureResource(object):
    """
    Represents a Face Capture resource object.
    """

    def __init__(self, session_id=None, payload=None):
        self.__session_id = session_id
        self.__payload = payload

    @property
    def session_id(self):
        return self.__session_id

    @property
    def payload(self):
        return self.__payload

    @classmethod
    def build(cls, session_id, face_capture_response):
        return cls(
            session_id=session_id,
            payload={
                "image": face_capture_response.image,
                "tasks": face_capture_response.tasks,
                "source": face_capture_response.source,
            }
        )