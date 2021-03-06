import unittest

from yoti_python_sdk.doc_scan.session.retrieve.document_fields_response import (
    DocumentFieldsResponse,
)
from yoti_python_sdk.doc_scan.session.retrieve.document_id_photo_response import (
    DocumentIdPhotoResponse,
)
from yoti_python_sdk.doc_scan.session.retrieve.id_document_resource_response import (
    IdDocumentResourceResponse,
)
from yoti_python_sdk.doc_scan.session.retrieve.task_response import (
    TextExtractionTaskResponse,
    TaskResponse,
)


class IdDocumentResourceResponseTest(unittest.TestCase):
    SOME_ID = "someId"
    SOME_DOCUMENT_TYPE = "someDocumentType"
    SOME_ISSUING_COUNTRY = "someIssuingCountry"
    SOME_TASKS = [
        {"first": "task", "type": "ID_DOCUMENT_TEXT_DATA_EXTRACTION"},
        {"second": "task"},
    ]
    SOME_PAGES = [{"first": "page"}, {"second": "page"}]
    SOME_DOCUMENT_FIELDS = {"media": {}}
    SOME_DOCUMENT_ID_PHOTO = {"media": {}}

    def test_should_parse_correctly(self):
        data = {
            "id": self.SOME_ID,
            "document_type": self.SOME_DOCUMENT_TYPE,
            "issuing_country": self.SOME_ISSUING_COUNTRY,
            "tasks": self.SOME_TASKS,
            "pages": self.SOME_PAGES,
            "document_fields": self.SOME_DOCUMENT_FIELDS,
            "document_id_photo": self.SOME_DOCUMENT_ID_PHOTO,
        }

        result = IdDocumentResourceResponse(data)

        assert result.id == self.SOME_ID
        assert result.document_type == self.SOME_DOCUMENT_TYPE
        assert result.issuing_country == self.SOME_ISSUING_COUNTRY
        assert len(result.tasks) == 2
        assert len(result.pages) == 2
        assert isinstance(result.document_fields, DocumentFieldsResponse)
        assert isinstance(result.document_id_photo, DocumentIdPhotoResponse)

    def test_should_parse_when_none(self):
        result = IdDocumentResourceResponse(None)

        assert result.id is None
        assert result.document_type is None
        assert result.issuing_country is None
        assert len(result.tasks) == 0
        assert len(result.pages) == 0
        assert result.document_fields is None
        assert result.document_id_photo is None

    def test_should_parse_tasks_with_type(self):
        data = {
            "id": self.SOME_ID,
            "document_type": self.SOME_DOCUMENT_TYPE,
            "issuing_country": self.SOME_ISSUING_COUNTRY,
            "tasks": self.SOME_TASKS,
            "pages": self.SOME_PAGES,
            "document_fields": self.SOME_DOCUMENT_FIELDS,
        }

        result = IdDocumentResourceResponse(data)

        assert len(result.tasks) == 2
        assert isinstance(result.tasks[0], TextExtractionTaskResponse)
        assert isinstance(result.tasks[1], TaskResponse)

    def test_should_filter_text_extraction_tasks(self):
        data = {"tasks": self.SOME_TASKS}

        result = IdDocumentResourceResponse(data)

        assert len(result.tasks) == 2
        assert len(result.text_extraction_tasks) == 1


if __name__ == "__main__":
    unittest.main()
