import json
import unittest

from yoti_python_sdk.doc_scan.session.create.task import (
    RequestedSupplementaryDocTextExtractionTaskBuilder,
)
from yoti_python_sdk.doc_scan.session.create.task.requested_task import RequestedTask
from yoti_python_sdk.doc_scan.session.create.task.supplementary_doc_text_extraction import (
    RequestedSupplementaryDocTextExtractionTask,
    RequestedSupplementaryDocTextExtractionTaskConfig,
)

from yoti_python_sdk.utils import YotiEncoder


class RequestedSupplementaryDocTextExtractionTaskTest(unittest.TestCase):
    def test_should_build_text_data_extraction_task(self):
        result = RequestedSupplementaryDocTextExtractionTaskBuilder().build()

        assert isinstance(result, RequestedTask)
        assert isinstance(result, RequestedSupplementaryDocTextExtractionTask)
        assert isinstance(
            result.config, RequestedSupplementaryDocTextExtractionTaskConfig
        )

        assert result.type == "SUPPLEMENTARY_DOCUMENT_TEXT_DATA_EXTRACTION"

    def test_should_build_with_manual_check_always(self):
        result = (
            RequestedSupplementaryDocTextExtractionTaskBuilder()
            .with_manual_check_always()
            .build()
        )

        assert result.config.manual_check == "ALWAYS"

    def test_should_build_with_manual_check_fallback(self):
        result = (
            RequestedSupplementaryDocTextExtractionTaskBuilder()
            .with_manual_check_fallback()
            .build()
        )

        assert result.config.manual_check == "FALLBACK"

    def test_should_build_with_manual_check_never(self):
        result = (
            RequestedSupplementaryDocTextExtractionTaskBuilder()
            .with_manual_check_never()
            .build()
        )

        assert result.config.manual_check == "NEVER"

    def test_should_serialize_to_json_without_error(self):
        result = (
            RequestedSupplementaryDocTextExtractionTaskBuilder()
            .with_manual_check_never()
            .build()
        )

        s = json.dumps(result, cls=YotiEncoder)
        assert s is not None and s != ""

    def test_to_json_should_return_correct_properties(self):
        result = (
            RequestedSupplementaryDocTextExtractionTaskBuilder()
            .with_manual_check_always()
            .build()
        )

        json = result.to_json()
        assert json is not None

        json_config = json.get("config").to_json()
        assert json_config.get("manual_check") == "ALWAYS"

    def test_to_json_should_not_include_null_config_values(self):
        result = RequestedSupplementaryDocTextExtractionTaskBuilder().build()

        json = result.to_json()
        assert json is not None

        json_config = json.get("config").to_json()
        assert json_config == {}


if __name__ == "__main__":
    unittest.main()
