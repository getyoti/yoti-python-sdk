import unittest
from datetime import datetime

import pytz

from yoti_python_sdk.doc_scan.session.retrieve.media_response import MediaResponse


class MediaResponseTest(unittest.TestCase):
    SOME_ID = "someId"
    SOME_TYPE = "someType"
    SOME_CREATED = "2019-05-01T05:01:48.000Z"
    SOME_LAST_UPDATED = "2019-05-01T05:01:48.000Z"

    EXPECTED_DATETIME = datetime(
        year=2019,
        month=5,
        day=1,
        hour=5,
        minute=1,
        second=48,
        microsecond=0,
        tzinfo=pytz.utc,
    )

    def test_should_parse_correctly(self):
        data = {
            "id": self.SOME_ID,
            "type": self.SOME_TYPE,
            "created": self.SOME_CREATED,
            "last_updated": self.SOME_LAST_UPDATED,
        }

        result = MediaResponse(data)

        assert result.id is self.SOME_ID
        assert result.type is self.SOME_TYPE
        assert result.created == self.EXPECTED_DATETIME
        assert result.last_updated == self.EXPECTED_DATETIME

    def test_should_parse_with_none(self):
        result = MediaResponse(None)

        assert result.id is None
        assert result.type is None
        assert result.created is None
        assert result.last_updated is None

    def test_should_set_dates_as_none_for_invalid_format(self):
        data = {"created": "someInvalidFormat", "last_updated": "someInvalidFormat"}

        result = MediaResponse(data)

        assert result.created is None
        assert result.last_updated is None


if __name__ == "__main__":
    unittest.main()
