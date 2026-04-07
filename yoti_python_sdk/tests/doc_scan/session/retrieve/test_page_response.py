import unittest

from yoti_python_sdk.doc_scan.session.retrieve.media_response import MediaResponse
from yoti_python_sdk.doc_scan.session.retrieve.page_response import PageResponse
from yoti_python_sdk.doc_scan.session.retrieve.frame_response import FrameResponse


class PageResponseTest(unittest.TestCase):
    SOME_CAPTURE_METHOD = "someCaptureMethod"
    SOME_FRAMES = [{"first": "frame"}, {"second": "frame"}]
    SOME_EXTRACTION_IMAGE_IDS = [
        "066a9372-0a52-4fe4-a026-866f8aee6fcb",
        "9b0c9c0a-ff30-41ed-815b-d95d63271d45",
    ]

    def test_should_parse_correctly(self):
        data = {
            "capture_method": self.SOME_CAPTURE_METHOD,
            "media": {},
            "frames": self.SOME_FRAMES,
            "extraction_image_ids": self.SOME_EXTRACTION_IMAGE_IDS,
        }

        result = PageResponse(data)

        assert result.capture_method is self.SOME_CAPTURE_METHOD
        assert isinstance(result.media, MediaResponse)
        assert len(result.frames) == 2
        assert isinstance(result.frames[0], FrameResponse)
        assert isinstance(result.frames[1], FrameResponse)
        assert len(result.extraction_image_ids) == 2
        assert result.extraction_image_ids == self.SOME_EXTRACTION_IMAGE_IDS

    def test_should_parse_with_none(self):
        result = PageResponse(None)

        assert result.capture_method is None
        assert result.media is None
        assert len(result.frames) == 0
        assert len(result.extraction_image_ids) == 0


if __name__ == "__main__":
    unittest.main()
