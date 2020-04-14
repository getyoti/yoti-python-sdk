import base64
import unittest

from yoti_python_sdk.doc_scan.session.retrieve.media_value import MediaValue


class MediaValueTest(unittest.TestCase):
    SOME_MIME_TYPE = "someMimeType"
    SOME_CONTENT = b"someByteArray"

    def test_should_parse_correctly(self):
        result = MediaValue(self.SOME_MIME_TYPE, self.SOME_CONTENT)

        assert result.mime_type is self.SOME_MIME_TYPE
        assert result.content is self.SOME_CONTENT

        expected = (
            "data:"
            + self.SOME_MIME_TYPE
            + ";base64,"
            + base64.b64encode(self.SOME_CONTENT).decode("utf-8")
        )

        assert result.base64_content == expected


if __name__ == "__main__":
    unittest.main()
