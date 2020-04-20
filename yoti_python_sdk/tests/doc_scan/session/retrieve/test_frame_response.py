import unittest

from yoti_python_sdk.doc_scan.session.retrieve.frame_response import FrameResponse
from yoti_python_sdk.doc_scan.session.retrieve.media_response import MediaResponse


class FrameResponseTest(unittest.TestCase):
    def test_should_parse_correctly(self):
        data = {"media": {}}

        result = FrameResponse(data)
        assert isinstance(result.media, MediaResponse)

    def test_should_parse_when_none(self):
        result = FrameResponse(None)
        assert isinstance(result, FrameResponse)
        assert result.media is None


if __name__ == "__main__":
    unittest.main()
