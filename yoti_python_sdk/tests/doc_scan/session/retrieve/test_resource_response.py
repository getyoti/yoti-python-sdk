import unittest

from yoti_python_sdk.doc_scan.session.retrieve.resource_response import ResourceResponse
from yoti_python_sdk.doc_scan.session.retrieve.task_response import TaskResponse
from yoti_python_sdk.doc_scan.session.retrieve.task_response import (
    TextExtractionTaskResponse,
)


class ResourceResponseTest(unittest.TestCase):
    SOME_ID = "someId"

    def test_should_parse_correctly(self):
        data = {
            "id": self.SOME_ID,
            "tasks": [
                {"type": "ID_DOCUMENT_TEXT_DATA_EXTRACTION"},
                {"type": "someUnknownType"},
            ],
        }

        result = ResourceResponse(data)

        assert result.id is self.SOME_ID
        assert len(result.tasks) == 2
        assert isinstance(result.tasks[0], TextExtractionTaskResponse)
        assert isinstance(result.tasks[1], TaskResponse)

    def test_should_parse_with_none(self):
        result = ResourceResponse(None)

        assert result.id is None
        assert len(result.tasks) == 0


if __name__ == "__main__":
    unittest.main()
