import json
import unittest

from yoti_python_sdk.doc_scan.session.create.check import (
    RequestedDocumentAuthenticityCheckBuilder,
)
from yoti_python_sdk.doc_scan.session.create.check.document_authenticity import (
    RequestedDocumentAuthenticityCheck,
)
from yoti_python_sdk.doc_scan.session.create.check.document_authenticity import (
    RequestedDocumentAuthenticityCheckConfig,
)
from yoti_python_sdk.doc_scan.session.create.check.requested_check import RequestedCheck
from yoti_python_sdk.utils import YotiEncoder


class RequestedDocumentAuthenticityCheckTest(unittest.TestCase):
    def test_should_build_correctly(self):
        result = RequestedDocumentAuthenticityCheckBuilder().build()

        assert isinstance(result, RequestedCheck)
        assert isinstance(result, RequestedDocumentAuthenticityCheck)
        assert isinstance(result.config, RequestedDocumentAuthenticityCheckConfig)
        assert result.type == "ID_DOCUMENT_AUTHENTICITY"

    def test_should_serialize_to_json_without_error(self):
        result = RequestedDocumentAuthenticityCheckBuilder().build()

        s = json.dumps(result, cls=YotiEncoder)
        assert s is not None and s != ""

    def test_should_build_with_manual_check_always(self):
        result = (
            RequestedDocumentAuthenticityCheckBuilder()
            .with_manual_check_always()
            .build()
        )

        assert result.config.manual_check == "ALWAYS"

    def test_should_build_with_manual_check_fallback(self):
        result = (
            RequestedDocumentAuthenticityCheckBuilder()
            .with_manual_check_fallback()
            .build()
        )

        assert result.config.manual_check == "FALLBACK"

    def test_should_build_with_manual_check_never(self):
        result = (
            RequestedDocumentAuthenticityCheckBuilder()
            .with_manual_check_never()
            .build()
        )

        assert result.config.manual_check == "NEVER"


if __name__ == "__main__":
    unittest.main()
