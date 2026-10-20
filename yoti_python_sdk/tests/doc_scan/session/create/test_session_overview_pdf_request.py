import json
import unittest

from yoti_python_sdk.doc_scan.session.create.session_overview_pdf_request import (
    SessionOverviewPdfRequest,
    SessionOverviewPdfRequestBuilder,
)
from yoti_python_sdk.utils import YotiEncoder


class SessionOverviewPdfRequestTest(unittest.TestCase):
    def test_should_build_with_no_flags_set(self):
        result = SessionOverviewPdfRequestBuilder().build()

        assert isinstance(result, SessionOverviewPdfRequest)
        assert result.include_images is None
        assert result.include_extracted_text is None
        assert result.include_device_tracking is None

    def test_should_build_with_include_images_true(self):
        result = SessionOverviewPdfRequestBuilder().with_include_images(True).build()

        assert result.include_images is True

    def test_should_build_with_include_images_false(self):
        result = SessionOverviewPdfRequestBuilder().with_include_images(False).build()

        assert result.include_images is False

    def test_should_build_with_include_extracted_text_true(self):
        result = (
            SessionOverviewPdfRequestBuilder().with_include_extracted_text(True).build()
        )

        assert result.include_extracted_text is True

    def test_should_build_with_include_extracted_text_false(self):
        result = (
            SessionOverviewPdfRequestBuilder()
            .with_include_extracted_text(False)
            .build()
        )

        assert result.include_extracted_text is False

    def test_should_build_with_include_device_tracking_true(self):
        result = (
            SessionOverviewPdfRequestBuilder()
            .with_include_device_tracking(True)
            .build()
        )

        assert result.include_device_tracking is True

    def test_should_build_with_include_device_tracking_false(self):
        result = (
            SessionOverviewPdfRequestBuilder()
            .with_include_device_tracking(False)
            .build()
        )

        assert result.include_device_tracking is False

    def test_should_omit_all_keys_when_no_flags_set(self):
        """Unprovided flags must be omitted from JSON, not sent as false/null."""
        result = SessionOverviewPdfRequestBuilder().build()

        serialized = json.dumps(result, cls=YotiEncoder)
        parsed = json.loads(serialized)

        assert "include_images" not in parsed
        assert "include_extracted_text" not in parsed
        assert "include_device_tracking" not in parsed

    def test_should_include_all_keys_when_all_flags_set(self):
        result = (
            SessionOverviewPdfRequestBuilder()
            .with_include_images(True)
            .with_include_extracted_text(True)
            .with_include_device_tracking(True)
            .build()
        )

        serialized = json.dumps(result, cls=YotiEncoder)
        parsed = json.loads(serialized)

        assert parsed["include_images"] is True
        assert parsed["include_extracted_text"] is True
        assert parsed["include_device_tracking"] is True

    def test_should_omit_unset_keys_when_only_subset_provided(self):
        """Only the keys that were explicitly set should appear in the JSON."""
        result = SessionOverviewPdfRequestBuilder().with_include_images(True).build()

        serialized = json.dumps(result, cls=YotiEncoder)
        parsed = json.loads(serialized)

        assert "include_images" in parsed
        assert parsed["include_images"] is True
        assert "include_extracted_text" not in parsed
        assert "include_device_tracking" not in parsed

    def test_should_serialize_false_value_when_explicitly_set(self):
        """
        An explicitly-set False should appear in the JSON (it's a deliberate
        choice by the caller, not an absence of a value).
        """
        result = SessionOverviewPdfRequestBuilder().with_include_images(False).build()

        serialized = json.dumps(result, cls=YotiEncoder)
        parsed = json.loads(serialized)

        assert "include_images" in parsed
        assert parsed["include_images"] is False

    def test_should_use_snake_case_json_keys(self):
        result = (
            SessionOverviewPdfRequestBuilder()
            .with_include_images(True)
            .with_include_extracted_text(True)
            .with_include_device_tracking(True)
            .build()
        )

        serialized = json.dumps(result, cls=YotiEncoder)

        assert "include_images" in serialized
        assert "include_extracted_text" in serialized
        assert "include_device_tracking" in serialized


if __name__ == "__main__":
    unittest.main()
