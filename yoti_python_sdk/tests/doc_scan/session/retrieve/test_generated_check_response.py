import unittest

from yoti_python_sdk.doc_scan.session.retrieve.generated_check_response import (
    GeneratedCheckResponse,
)


class GeneratedCheckResponseTest(unittest.TestCase):
    SOME_ID = "someId"
    SOME_TYPE = "someType"

    def test_should_parse_correctly(self):
        data = {"id": self.SOME_ID, "type": self.SOME_TYPE}

        result = GeneratedCheckResponse(data)

        assert result.id is self.SOME_ID
        assert result.type is self.SOME_TYPE

    def test_should_parse_when_none(self):
        result = GeneratedCheckResponse(None)

        assert isinstance(result, GeneratedCheckResponse)
        assert result.id is None
        assert result.type is None


if __name__ == "__main__":
    unittest.main()
