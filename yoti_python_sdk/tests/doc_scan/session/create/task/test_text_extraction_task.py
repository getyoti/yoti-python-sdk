import json
import unittest

from yoti_python_sdk.doc_scan.session.create.task import (
    RequestedTextExtractionTaskBuilder,
)
from yoti_python_sdk.doc_scan.session.create.task.requested_task import RequestedTask
from yoti_python_sdk.doc_scan.session.create.task.text_extraction import (
    RequestedTextExtractionTask,
)
from yoti_python_sdk.doc_scan.session.create.task.text_extraction import (
    RequestedTextExtractionTaskConfig,
)
from yoti_python_sdk.utils import YotiEncoder


class RequestedTextExtractionTaskTest(unittest.TestCase):
    def test_should_build_with_manual_check_always(self):
        result = RequestedTextExtractionTaskBuilder().with_manual_check_always().build()

        assert isinstance(result, RequestedTask)
        assert isinstance(result, RequestedTextExtractionTask)
        assert isinstance(result.config, RequestedTextExtractionTaskConfig)

        assert result.type == "ID_DOCUMENT_TEXT_DATA_EXTRACTION"
        assert result.config.manual_check == "ALWAYS"

    def test_should_build_with_manual_check_fallback(self):
        result = (
            RequestedTextExtractionTaskBuilder().with_manual_check_fallback().build()
        )

        assert result.config.manual_check == "FALLBACK"

    def test_should_build_with_manual_check_never(self):
        result = RequestedTextExtractionTaskBuilder().with_manual_check_never().build()

        assert result.config.manual_check == "NEVER"

    def test_should_serialize_to_json_without_error(self):
        result = RequestedTextExtractionTaskBuilder().with_manual_check_never().build()

        s = json.dumps(result, cls=YotiEncoder)
        assert s is not None and s != ""


if __name__ == "__main__":
    unittest.main()
