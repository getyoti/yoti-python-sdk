import unittest

from yoti_python_sdk.doc_scan.session.retrieve.media_response import MediaResponse
from yoti_python_sdk.doc_scan.session.retrieve.share_code_media_response import (
    ShareCodeMediaResponse,
)


class ShareCodeMediaResponseTest(unittest.TestCase):
    def test_should_parse_media(self):
        data = {"media": {"id": "some-media-id", "type": "JSON"}}

        result = ShareCodeMediaResponse(data)

        assert isinstance(result.media, MediaResponse)
        assert result.media.id == "some-media-id"
        assert result.media.type == "JSON"

    def test_should_return_none_media_when_key_missing(self):
        result = ShareCodeMediaResponse({})

        assert result.media is None

    def test_should_parse_when_none(self):
        result = ShareCodeMediaResponse(None)

        assert result.media is None

    def test_should_parse_empty_media(self):
        data = {"media": {}}

        result = ShareCodeMediaResponse(data)

        assert isinstance(result.media, MediaResponse)
        assert result.media.id is None
        assert result.media.type is None

    def test_should_return_none_media_when_value_is_null(self):
        data = {"media": None}

        result = ShareCodeMediaResponse(data)

        assert result.media is None


if __name__ == "__main__":
    unittest.main()
