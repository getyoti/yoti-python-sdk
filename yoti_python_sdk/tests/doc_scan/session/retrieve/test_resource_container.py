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
from yoti_python_sdk.doc_scan.session.retrieve.static_liveness_resource_response import (
    StaticLivenessResourceResponse,
)
from yoti_python_sdk.doc_scan.session.retrieve.share_code_resource_response import (
    ShareCodeResourceResponse,
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

    def test_should_filter_static_liveness_resources(self):
        data = {
            "liveness_capture": [
                {"liveness_type": "STATIC"},
                {"liveness_type": "someUnknown"},
            ]
        }

        result = ResourceContainer(data)

        assert len(result.liveness_capture) == 2
        assert len(result.static_liveness_resources) == 1

    def test_should_expose_capture_type_on_static_liveness_resource(self):
        data = {
            "liveness_capture": [
                {"liveness_type": "STATIC", "capture_type": "PHOTOGRAPH"},
                {"liveness_type": "ZOOM"},
            ]
        }

        result = ResourceContainer(data)

        static_resources = result.static_liveness_resources
        assert len(static_resources) == 1
        assert isinstance(static_resources[0], StaticLivenessResourceResponse)
        assert static_resources[0].capture_type == "PHOTOGRAPH"

        zoom_resources = result.zoom_liveness_resources
        assert len(zoom_resources) == 1
        assert not hasattr(zoom_resources[0], "capture_type")

    def test_should_parse_share_codes(self):
        data = {
            "share_codes": [
                {"id": "share-code-1", "source": "END_USER", "tasks": []},
                {"id": "share-code-2", "source": "END_USER", "tasks": []},
            ]
        }

        result = ResourceContainer(data)

        assert len(result.share_codes) == 2
        assert isinstance(result.share_codes[0], ShareCodeResourceResponse)
        assert isinstance(result.share_codes[1], ShareCodeResourceResponse)

    def test_should_parse_with_empty_share_codes(self):
        data = {"share_codes": []}

        result = ResourceContainer(data)

        assert len(result.share_codes) == 0

    def test_should_parse_with_missing_share_codes(self):
        result = ResourceContainer({})

        assert len(result.share_codes) == 0


if __name__ == "__main__":
    unittest.main()
