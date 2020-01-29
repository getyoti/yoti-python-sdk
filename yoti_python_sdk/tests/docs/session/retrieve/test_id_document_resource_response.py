import unittest

from yoti_python_sdk.docs.session.retrieve.document_fields_response import (
    DocumentFieldsResponse,
)
from yoti_python_sdk.docs.session.retrieve.id_document_resource_response import (
    IdDocumentResourceResponse,
)


class IdDocumentResourceResponseTest(unittest.TestCase):
    SOME_ID = "someId"
    SOME_DOCUMENT_TYPE = "someDocumentType"
    SOME_ISSUING_COUNTRY = "someIssuingCountry"
    SOME_TASKS = [{"first": "task"}, {"second": "task"}]
    SOME_PAGES = [{"first": "page"}, {"second": "page"}]
    SOME_DOCUMENT_FIELDS = {"media": {}}

    def test_should_parse_correctly(self):
        data = {
            "id": self.SOME_ID,
            "document_type": self.SOME_DOCUMENT_TYPE,
            "issuing_country": self.SOME_ISSUING_COUNTRY,
            "tasks": self.SOME_TASKS,
            "pages": self.SOME_PAGES,
            "document_fields": self.SOME_DOCUMENT_FIELDS,
        }

        result = IdDocumentResourceResponse(data)

        assert result.id is self.SOME_ID
        assert result.document_type is self.SOME_DOCUMENT_TYPE
        assert result.issuing_country is self.SOME_ISSUING_COUNTRY
        assert len(result.tasks) == 2
        assert len(result.pages) == 2
        assert isinstance(result.document_fields, DocumentFieldsResponse)

    def test_should_parse_when_none(self):
        result = IdDocumentResourceResponse(None)

        assert result.id is None
        assert result.document_type is None
        assert result.issuing_country is None
        assert len(result.tasks) == 0
        assert len(result.pages) == 0
        assert result.document_fields is None


if __name__ == "__main__":
    unittest.main()
