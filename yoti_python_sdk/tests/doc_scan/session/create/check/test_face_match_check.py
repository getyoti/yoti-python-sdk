import json
import unittest

from yoti_python_sdk.doc_scan.session.create import RequestedFaceMatchCheckBuilder
from yoti_python_sdk.doc_scan.session.create.check.face_match import (
    RequestedFaceMatchCheck,
)
from yoti_python_sdk.doc_scan.session.create.check.face_match import (
    RequestedFaceMatchCheckConfig,
)
from yoti_python_sdk.doc_scan.session.create.check.requested_check import RequestedCheck
from yoti_python_sdk.utils import YotiEncoder


class RequestedFaceMatchCheckTest(unittest.TestCase):
    def test_should_build_with_manual_check_always(self):
        result = RequestedFaceMatchCheckBuilder().with_manual_check_always().build()

        assert isinstance(result, RequestedCheck)
        assert isinstance(result, RequestedFaceMatchCheck)
        assert isinstance(result.config, RequestedFaceMatchCheckConfig)

        assert result.type == "ID_DOCUMENT_FACE_MATCH"
        assert result.config.manual_check == "ALWAYS"

    def test_should_build_with_manual_check_fallback(self):
        result = RequestedFaceMatchCheckBuilder().with_manual_check_fallback().build()

        assert result.config.manual_check == "FALLBACK"

    def test_should_build_with_manual_check_never(self):
        result = RequestedFaceMatchCheckBuilder().with_manual_check_never().build()

        assert result.config.manual_check == "NEVER"

    def test_should_serialize_to_json_without_error(self):
        result = RequestedFaceMatchCheckBuilder().with_manual_check_never().build()

        s = json.dumps(result, cls=YotiEncoder)
        assert s is not None and s != ""


if __name__ == "__main__":
    unittest.main()
