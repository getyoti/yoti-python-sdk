import unittest

from yoti_python_sdk.doc_scan.session.retrieve.media_response import MediaResponse
from yoti_python_sdk.doc_scan.session.retrieve.page_response import PageResponse


class PageResponseTest(unittest.TestCase):
    SOME_CAPTURE_METHOD = "someCaptureMethod"

    def test_should_parse_correctly(self):
        data = {"capture_method": self.SOME_CAPTURE_METHOD, "media": {}}

        result = PageResponse(data)

        assert result.capture_method is self.SOME_CAPTURE_METHOD
        assert isinstance(result.media, MediaResponse)

    def test_should_parse_with_none(self):
        result = PageResponse(None)

        assert result.capture_method is None
        assert result.media is None


if __name__ == "__main__":
    unittest.main()
