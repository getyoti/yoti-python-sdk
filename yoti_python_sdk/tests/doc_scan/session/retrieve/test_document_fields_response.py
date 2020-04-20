import unittest

from yoti_python_sdk.doc_scan.session.retrieve.document_fields_response import (
    DocumentFieldsResponse,
)
from yoti_python_sdk.doc_scan.session.retrieve.media_response import MediaResponse


class DocumentFieldsResponseTest(unittest.TestCase):
    def test_should_parse_correctly(self):
        data = {"media": {}}

        result = DocumentFieldsResponse(data)
        assert isinstance(result.media, MediaResponse)

    def test_should_not_throw_exception_for_none(self):
        result = DocumentFieldsResponse(None)
        assert result.media is None


if __name__ == "__main__":
    unittest.main()
