import unittest
from datetime import datetime

import pytz

from yoti_python_sdk.doc_scan.session.retrieve.check_response import CheckResponse
from yoti_python_sdk.doc_scan.session.retrieve.generated_media import GeneratedMedia
from yoti_python_sdk.doc_scan.session.retrieve.report_response import ReportResponse


class CheckResponseTest(unittest.TestCase):
    SOME_ID = "someId"
    SOME_STATE = "someState"
    SOME_TYPE = "someType"
    SOME_RESOURCES_USED = ["someFirstId", "someSecondId"]
    SOME_REPORT = {}
    SOME_GENERATED_MEDIA = [{"someKey": "someValue"}]
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

    def test_should_build_correctly(self):
        data = {
            "id": self.SOME_ID,
            "state": self.SOME_STATE,
            "type": self.SOME_TYPE,
            "resources_used": self.SOME_RESOURCES_USED,
            "report": self.SOME_REPORT,
            "generated_media": self.SOME_GENERATED_MEDIA,
            "created": self.SOME_CREATED,
            "last_updated": self.SOME_LAST_UPDATED,
        }

        result = CheckResponse(data)

        assert result.id is self.SOME_ID
        assert result.state is self.SOME_STATE
        assert result.type is self.SOME_TYPE
        assert len(result.resources_used) == 2
        assert isinstance(result.report, ReportResponse)
        assert len(result.generated_media) == 1
        assert isinstance(result.generated_media[0], GeneratedMedia)
        assert isinstance(result.created, datetime)

        assert result.created == self.EXPECTED_DATETIME
        assert result.last_updated == self.EXPECTED_DATETIME

    def test_should_default_relevant_properties_to_empty_list(self):
        result = CheckResponse({})

        assert len(result.resources_used) == 0
        assert len(result.generated_media) == 0

    def test_should_default_data_if_none(self):
        result = CheckResponse(None)

        assert result.id is None
        assert result.state is None
        assert result.type is None
        assert result.created is None
        assert result.last_updated is None
        assert len(result.resources_used) == 0
        assert len(result.generated_media) == 0

    def test_should_set_dates_to_none_if_invalid_format(self):
        data = {"created": "someInvalidDate", "last_updated": "someInvalidDate"}

        result = CheckResponse(data)

        assert result.created is None
        assert result.last_updated is None


if __name__ == "__main__":
    unittest.main()
