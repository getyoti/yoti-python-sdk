import unittest

from yoti_python_sdk.doc_scan.session.retrieve.face_map_response import FaceMapResponse
from yoti_python_sdk.doc_scan.session.retrieve.media_response import MediaResponse


class FaceMapResponseTest(unittest.TestCase):
    def test_should_build_correctly(self):
        data = {"media": {}}

        result = FaceMapResponse(data)
        assert isinstance(result.media, MediaResponse)

    def test_should_parse_with_none(self):
        result = FaceMapResponse(None)
        assert result.media is None


if __name__ == "__main__":
    unittest.main()
