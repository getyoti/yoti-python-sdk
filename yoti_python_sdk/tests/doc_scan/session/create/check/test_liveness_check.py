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

    def test_should_build_with_static_liveness_type(self):
        result = (
            RequestedLivenessCheckBuilder()
            .for_static_liveness()
            .with_max_retries(3)
            .build()
        )

        assert result.type == "LIVENESS"
        assert result.config.liveness_type == "STATIC"
        assert result.config.max_retries == 3

    def test_should_build_with_manual_check_never(self):
        result = (
            RequestedLivenessCheckBuilder()
            .for_static_liveness()
            .with_max_retries(3)
            .with_manual_check_never()
            .build()
        )

        assert result.config.liveness_type == "STATIC"
        assert result.config.manual_check == "NEVER"

    def test_should_serialize_static_liveness_to_json(self):
        result = (
            RequestedLivenessCheckBuilder()
            .for_static_liveness()
            .with_max_retries(3)
            .with_manual_check_never()
            .build()
        )

        json_str = json.dumps(result, cls=YotiEncoder)
        assert json_str is not None
        
        # Verify the JSON contains the expected fields
        json_data = json.loads(json_str)
        assert json_data["type"] == "LIVENESS"
        assert json_data["config"]["liveness_type"] == "STATIC"
        assert json_data["config"]["manual_check"] == "NEVER"
        assert json_data["config"]["max_retries"] == 3

    def test_should_omit_manual_check_when_not_set(self):
        result = (
            RequestedLivenessCheckBuilder()
            .for_static_liveness()
            .with_max_retries(3)
            .build()
        )

        json_str = json.dumps(result, cls=YotiEncoder)
        assert json_str is not None
        
        # Verify the JSON does not contain the manual_check field
        json_data = json.loads(json_str)
        assert json_data["type"] == "LIVENESS"
        assert json_data["config"]["liveness_type"] == "STATIC"
        assert "manual_check" not in json_data["config"]
        assert json_data["config"]["max_retries"] == 3


if __name__ == "__main__":
    unittest.main()
