import unittest

from yoti_python_sdk.doc_scan.session.retrieve.file_response import FileResponse
from yoti_python_sdk.doc_scan.session.retrieve.media_response import MediaResponse


class FileResponseTest(unittest.TestCase):
    def test_should_parse_correctly(self):
        data = {"media": {}}

        result = FileResponse(data)
        assert isinstance(result.media, MediaResponse)

    def test_should_parse_when_none(self):
        result = FileResponse(None)
        assert isinstance(result, FileResponse)
        assert result.media is None


if __name__ == "__main__":
    unittest.main()
