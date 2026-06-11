import unittest

from yoti_python_sdk.doc_scan.session.retrieve.media_response import MediaResponse
from yoti_python_sdk.doc_scan.session.retrieve.page_response import PageResponse
from yoti_python_sdk.doc_scan.session.retrieve.frame_response import FrameResponse


class PageResponseTest(unittest.TestCase):
    SOME_CAPTURE_METHOD = "someCaptureMethod"
    SOME_FRAMES = [{"first": "frame"}, {"second": "frame"}]
    SOME_EXTRACTION_IMAGE_ID = "066a9372-1ab9-49f0-b390-1b58e08f17f6"
    SOME_OTHER_EXTRACTION_IMAGE_ID = "1a2b3c4d-5e6f-7890-abcd-ef1234567890"

    def test_should_parse_correctly(self):
        data = {
            "capture_method": self.SOME_CAPTURE_METHOD,
            "media": {},
            "frames": self.SOME_FRAMES,
            "extraction_image_ids": [
                self.SOME_EXTRACTION_IMAGE_ID,
                self.SOME_OTHER_EXTRACTION_IMAGE_ID,
            ],
        }

        result = PageResponse(data)

        assert result.capture_method is self.SOME_CAPTURE_METHOD
        assert isinstance(result.media, MediaResponse)
        assert len(result.frames) == 2
        assert isinstance(result.frames[0], FrameResponse)
        assert isinstance(result.frames[1], FrameResponse)
        assert result.extraction_image_ids == [
            self.SOME_EXTRACTION_IMAGE_ID,
            self.SOME_OTHER_EXTRACTION_IMAGE_ID,
        ]

    def test_should_parse_with_none(self):
        result = PageResponse(None)

        assert result.capture_method is None
        assert result.media is None
        assert len(result.frames) == 0
        assert result.extraction_image_ids == []

    def test_should_parse_extraction_image_ids_with_single_uuid(self):
        data = {"extraction_image_ids": [self.SOME_EXTRACTION_IMAGE_ID]}

        result = PageResponse(data)

        assert result.extraction_image_ids == [self.SOME_EXTRACTION_IMAGE_ID]

    def test_should_parse_extraction_image_ids_with_empty_array(self):
        data = {"extraction_image_ids": []}

        result = PageResponse(data)

        assert result.extraction_image_ids == []

    def test_should_parse_extraction_image_ids_with_null(self):
        data = {"extraction_image_ids": None}

        result = PageResponse(data)

        assert result.extraction_image_ids == []

    def test_should_parse_extraction_image_ids_when_field_absent(self):
        data = {"capture_method": self.SOME_CAPTURE_METHOD}

        result = PageResponse(data)

        assert result.extraction_image_ids == []


if __name__ == "__main__":
    unittest.main()
