import unittest

from yoti_python_sdk.doc_scan.session.retrieve.generated_media import GeneratedMedia


class GeneratedMediaTest(unittest.TestCase):
    SOME_ID = "someId"
    SOME_TYPE = "someType"

    def test_should_parse_correctly(self):
        data = {"id": self.SOME_ID, "type": self.SOME_TYPE}

        result = GeneratedMedia(data)

        assert result.id is self.SOME_ID
        assert result.type is self.SOME_TYPE

    def test_should_parse_with_none(self):
        result = GeneratedMedia(None)

        assert isinstance(result, GeneratedMedia)
        assert result.id is None
        assert result.type is None


if __name__ == "__main__":
    unittest.main()
