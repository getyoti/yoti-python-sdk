import unittest

from yoti_python_sdk.doc_scan.session.retrieve.liveness_resource_response import (
    LivenessResourceResponse,
)
from yoti_python_sdk.doc_scan.session.retrieve.liveness_resource_response import (
    ZoomLivenessResourceResponse,
)
from yoti_python_sdk.doc_scan.session.retrieve.resource_container import (
    ResourceContainer,
)


class ResourceContainerTest(unittest.TestCase):
    def test_should_parse_correctly(self):
        data = {
            "id_documents": [{"first": "id_document"}, {"second": "id_document"}],
            "supplementary_documents": [{"first": "document"}, {"second": "document"}],
            "liveness_capture": [
                {"liveness_type": "ZOOM"},
                {"liveness_type": "someUnknown"},
            ],
        }

        result = ResourceContainer(data)

        assert len(result.id_documents) == 2
        assert len(result.supplementary_documents) == 2
        assert len(result.liveness_capture) == 2
        assert isinstance(result.liveness_capture[0], ZoomLivenessResourceResponse)
        assert isinstance(result.liveness_capture[1], LivenessResourceResponse)

    def test_should_parse_with_none(self):
        result = ResourceContainer(None)

        assert len(result.id_documents) == 0
        assert len(result.liveness_capture) == 0

    def test_should_filter_zoom_liveness_resources(self):
        data = {
            "liveness_capture": [
                {"liveness_type": "ZOOM"},
                {"liveness_type": "someUnknown"},
            ]
        }

        result = ResourceContainer(data)

        assert len(result.liveness_capture) == 2
        assert len(result.zoom_liveness_resources) == 1


if __name__ == "__main__":
    unittest.main()
