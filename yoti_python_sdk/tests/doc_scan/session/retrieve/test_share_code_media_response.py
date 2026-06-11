# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

from yoti_python_sdk.doc_scan.session.retrieve.share_code_media_response import (
    ShareCodeMediaResponse,
)


class ShareCodeMediaResponseTest(unittest.TestCase):
    def test_should_parse_media(self):
        data = {
            "media": {
                "id": "some-media-id",
                "type": "JSON",
                "created": "2026-02-05T11:33:46Z",
                "last_updated": "2026-02-05T11:33:50Z",
            }
        }

        result = ShareCodeMediaResponse(data)

        assert result.media is not None
        assert result.media.id == "some-media-id"
        assert result.media.type == "JSON"
        assert result.media.created is not None
        assert result.media.last_updated is not None

    def test_should_return_none_media_when_key_missing(self):
        result = ShareCodeMediaResponse({})

        assert result.media is None

    def test_should_return_none_media_when_value_is_null(self):
        data = {"media": None}

        result = ShareCodeMediaResponse(data)

        assert result.media is None

    def test_should_parse_empty_media_object(self):
        data = {"media": {}}

        result = ShareCodeMediaResponse(data)

        assert result.media is not None
        assert result.media.id is None
        assert result.media.type is None

    def test_should_parse_when_none(self):
        result = ShareCodeMediaResponse(None)

        assert result.media is None


if __name__ == "__main__":
    unittest.main()
