import json

from mock import Mock

from yoti_python_sdk.doc_scan.session.create.filter.document_filter import (
    DocumentFilter,
)
from yoti_python_sdk.doc_scan.session.create.filter.orthogonal_restrictions_filter import (
    OrthogonalRestrictionsFilter,
)
from yoti_python_sdk.doc_scan.session.create.filter.required_document import (
    RequiredDocument,
)
from yoti_python_sdk.doc_scan.session.create.filter.required_id_document import (
    RequiredIdDocument,
    RequiredIdDocumentBuilder,
)
from yoti_python_sdk.utils import YotiEncoder


def test_should_allow_direct_instantiation():
    doc_filter_mock = Mock(spec=OrthogonalRestrictionsFilter)

    result = RequiredIdDocument(doc_filter_mock)
    assert result.type == "ID_DOCUMENT"
    assert result.filter == doc_filter_mock


def test_builder_should_accept_any_document_filter():
    doc_filter = DocumentFilter("SOME_FILTER")

    result = RequiredIdDocumentBuilder().with_filter(doc_filter).build()

    assert isinstance(result, RequiredDocument)
    assert result.filter == doc_filter


def test_to_json_should_not_raise_exception():
    doc_filter = DocumentFilter("SOME_FILTER")

    result = RequiredIdDocumentBuilder().with_filter(doc_filter).build()

    s = json.dumps(result, cls=YotiEncoder)
    assert s is not None and s != ""
