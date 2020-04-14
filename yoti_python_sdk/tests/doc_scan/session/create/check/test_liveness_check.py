import unittest
import json

from yoti_python_sdk.doc_scan.session.create.check import RequestedLivenessCheckBuilder
from yoti_python_sdk.doc_scan.session.create.check.liveness import (
    RequestedLivenessCheck,
)
from yoti_python_sdk.doc_scan.session.create.check.liveness import (
    RequestedLivenessCheckConfig,
)
from yoti_python_sdk.doc_scan.session.create.check.requested_check import RequestedCheck
from yoti_python_sdk.utils import YotiEncoder


class RequestedLivenessCheckTest(unittest.TestCase):
    def test_should_build_correctly(self):
        result = (
            RequestedLivenessCheckBuilder()
            .with_liveness_type("SOME_LIVENESS_TYPE")
            .with_max_retries(3)
            .build()
        )

        assert isinstance(result, RequestedCheck)
        assert isinstance(result, RequestedLivenessCheck)
        assert isinstance(result.config, RequestedLivenessCheckConfig)

        assert result.type == "LIVENESS"
        assert result.config.liveness_type == "SOME_LIVENESS_TYPE"
        assert result.config.max_retries == 3

    def test_should_build_with_zoom_liveness_type(self):
        result = (
            RequestedLivenessCheckBuilder()
            .for_zoom_liveness()
            .with_max_retries(5)
            .build()
        )

        assert result.type == "LIVENESS"
        assert result.config.liveness_type == "ZOOM"
        assert result.config.max_retries == 5

    def test_should_serialize_to_json_without_error(self):
        result = (
            RequestedLivenessCheckBuilder()
            .for_zoom_liveness()
            .with_max_retries(5)
            .build()
        )

        s = json.dumps(result, cls=YotiEncoder)
        assert s is not None and s != ""


if __name__ == "__main__":
    unittest.main()
