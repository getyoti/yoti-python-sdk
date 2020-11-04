import unittest
from datetime import datetime

import pytz

from yoti_python_sdk.doc_scan.session.retrieve.generated_check_response import (
    GeneratedCheckResponse,
    GeneratedSupplementaryDocumentTextDataCheckResponse,
)
from yoti_python_sdk.doc_scan.session.retrieve.generated_check_response import (
    GeneratedTextDataCheckResponse,
)
from yoti_python_sdk.doc_scan.session.retrieve.task_response import (
    TaskResponse,
    TextExtractionTaskResponse,
    SupplementaryDocumentTextExtractionTaskResponse,
)


class TaskResponseTest(unittest.TestCase):
    SOME_ID = "someId"
    SOME_TYPE = "someType"
    SOME_STATE = "someState"

    SOME_GENERATED_CHECKS = [
        {"type": "ID_DOCUMENT_TEXT_DATA_CHECK"},
        {"type": "SUPPLEMENTARY_DOCUMENT_TEXT_DATA_CHECK"},
        {"type": "someUnknownType"},
    ]

    SOME_GENERATED_MEDIA = [{"first": "generated_media"}, {"second": "generated_media"}]

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
            "state": self.SOME_STATE,
            "created": self.SOME_CREATED,
            "last_updated": self.SOME_LAST_UPDATED,
            "generated_checks": self.SOME_GENERATED_CHECKS,
            "generated_media": self.SOME_GENERATED_MEDIA,
        }

        result = TaskResponse(data)

        assert result.id is self.SOME_ID
        assert result.type is self.SOME_TYPE
        assert result.state is self.SOME_STATE
        assert result.created == self.EXPECTED_DATETIME
        assert result.last_updated == self.EXPECTED_DATETIME

        assert len(result.generated_checks) == 3
        assert isinstance(result.generated_checks[0], GeneratedTextDataCheckResponse)
        assert isinstance(
            result.generated_checks[1],
            GeneratedSupplementaryDocumentTextDataCheckResponse,
        )
        assert isinstance(result.generated_checks[2], GeneratedCheckResponse)

        assert len(result.generated_media) == 2

    def test_should_parse_with_none(self):
        result = TaskResponse(None)

        assert result.id is None
        assert result.type is None
        assert result.state is None
        assert result.created is None
        assert result.last_updated is None
        assert len(result.generated_checks) == 0
        assert len(result.generated_media) == 0

    def test_should_filter_generated_text_data_checks(self):
        data = {"generated_checks": self.SOME_GENERATED_CHECKS}

        result = TextExtractionTaskResponse(data)

        assert len(result.generated_checks) == 3
        assert len(result.generated_text_data_checks) == 1
        assert isinstance(
            result.generated_text_data_checks[0], GeneratedTextDataCheckResponse
        )

    def test_supplementary_task_should_filter_generated_text_data_checks(self):
        data = {"generated_checks": self.SOME_GENERATED_CHECKS}

        result = SupplementaryDocumentTextExtractionTaskResponse(data)

        assert len(result.generated_checks) == 3
        assert len(result.generated_text_data_checks) == 1
        assert isinstance(
            result.generated_text_data_checks[0],
            GeneratedSupplementaryDocumentTextDataCheckResponse,
        )


if __name__ == "__main__":
    unittest.main()
