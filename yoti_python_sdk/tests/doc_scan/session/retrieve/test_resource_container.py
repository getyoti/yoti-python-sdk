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
            "share_codes": [
                {"id": "share-code-1", "source": "source-1"},
                {"id": "share-code-2", "source": "source-2"},
            ],
        }

        result = ResourceContainer(data)

        assert len(result.id_documents) == 2
        assert len(result.supplementary_documents) == 2
        assert len(result.liveness_capture) == 2
        assert isinstance(result.liveness_capture[0], ZoomLivenessResourceResponse)
        assert isinstance(result.liveness_capture[1], LivenessResourceResponse)
        assert len(result.share_codes) == 2
        assert isinstance(result.share_codes[0], ShareCodeResourceResponse)

    def test_should_parse_with_none(self):
        result = ResourceContainer(None)

        assert len(result.id_documents) == 0
        assert len(result.liveness_capture) == 0
        assert len(result.share_codes) == 0

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

    def test_should_parse_share_codes(self):
        data = {
            "share_codes": [
                {
                    "id": "share-code-id",
                    "source": "share-code-source",
                    "created_at": "2023-01-01T00:00:00Z",
                    "last_updated": "2023-01-02T00:00:00Z",
                }
            ]
        }

        result = ResourceContainer(data)

        assert len(result.share_codes) == 1
        assert result.share_codes[0].id == "share-code-id"
        assert result.share_codes[0].source == "share-code-source"


if __name__ == "__main__":
    unittest.main()
