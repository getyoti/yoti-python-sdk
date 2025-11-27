import unittest
from yoti_python_sdk.doc_scan.session.retrieve.static_liveness_resource_response import (
    StaticLivenessResourceResponse,
)
from yoti_python_sdk.doc_scan.session.retrieve.image_response import ImageResponse
from yoti_python_sdk.doc_scan.session.retrieve.media_response import MediaResponse


class StaticLivenessResourceResponseTest(unittest.TestCase):
    def test_should_parse_static_liveness_resource(self):
        data = {
            "id": "bbbbbbb-5717-4562-b3fc-2c963f66afa6",
            "source": {"type": "END_USER"},
            "liveness_type": "STATIC",
            "image": {
                "media": {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "type": "IMAGE",
                    "created": "2021-06-11T11:39:24Z",
                    "last_updated": "2021-06-11T11:39:24Z",
                }
            },
            "tasks": [],
        }

        result = StaticLivenessResourceResponse(data)

        assert result.id == "bbbbbbb-5717-4562-b3fc-2c963f66afa6"
        assert result.liveness_type == "STATIC"
        assert isinstance(result.image, ImageResponse)
        assert isinstance(result.image.media, MediaResponse)
        assert result.image.media.id == "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        assert result.image.media.type == "IMAGE"

    def test_should_handle_missing_image(self):
        data = {
            "id": "test-id",
            "liveness_type": "STATIC",
            "tasks": [],
        }

        result = StaticLivenessResourceResponse(data)

        assert result.id == "test-id"
        assert result.liveness_type == "STATIC"
        assert result.image is None

    def test_should_parse_media_id_for_retrieval(self):
        data = {
            "id": "resource-id",
            "liveness_type": "STATIC",
            "image": {
                "media": {
                    "id": "media-id-123",
                    "type": "IMAGE",
                    "created": "2021-06-11T11:39:24Z",
                    "last_updated": "2021-06-11T11:39:24Z",
                }
            },
            "tasks": [],
        }

        result = StaticLivenessResourceResponse(data)

        # Verify we can access the media ID for content retrieval
        assert result.image is not None
        assert result.image.media is not None
        assert result.image.media.id == "media-id-123"


if __name__ == "__main__":
    unittest.main()
