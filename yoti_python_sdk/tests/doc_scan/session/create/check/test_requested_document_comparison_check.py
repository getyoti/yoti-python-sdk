import json
import unittest

from yoti_python_sdk.doc_scan.session.create.check import (
    RequestedIDDocumentComparisonCheckBuilder,
)
from yoti_python_sdk.doc_scan.session.create.check.document_comparison import (
    RequestedIDDocumentComparisonCheck,
)
from yoti_python_sdk.doc_scan.session.create.check.document_comparison import (
    RequestedIDDocumentComparisonCheckConfig,
)
from yoti_python_sdk.doc_scan.session.create.check.document_comparison import (
    RequestedIDDocumentComparisonCheckBuilder,
)
from yoti_python_sdk.doc_scan.session.create.check.requested_check import RequestedCheck
from yoti_python_sdk.utils import YotiEncoder


def test_should_build_correctly():
    result = RequestedIDDocumentComparisonCheckBuilder().build()

    assert isinstance(result, RequestedCheck)
    assert isinstance(result, RequestedIDDocumentComparisonCheck)
    assert isinstance(result.config, RequestedIDDocumentComparisonCheckConfig)
    assert result.type == "ID_DOCUMENT_COMPARISON"


def test_should_serialize_to_json_without_error():
    result = RequestedIDDocumentComparisonCheckBuilder().build()

    s = json.dumps(result, cls=YotiEncoder)
    assert s is not None and s != ""
