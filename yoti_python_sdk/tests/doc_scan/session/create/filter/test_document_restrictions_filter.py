import json

from mock import Mock

from yoti_python_sdk.doc_scan.session.create.filter import (
    DocumentRestrictionsFilterBuilder,
)
from yoti_python_sdk.doc_scan.session.create.filter.document_restrictions_filter import (
    DocumentRestriction,
)
from yoti_python_sdk.utils import YotiEncoder


def test_should_set_inclusion_to_whitelist():
    result = DocumentRestrictionsFilterBuilder().for_whitelist().build()

    assert result.inclusion == "WHITELIST"


def test_should_set_inclusion_to_blacklist():
    result = DocumentRestrictionsFilterBuilder().for_blacklist().build()

    assert result.inclusion == "BLACKLIST"


def test_should_accept_document_restriction():
    document_restriction_mock = Mock(spec=DocumentRestriction)

    result = (
        DocumentRestrictionsFilterBuilder()
        .for_whitelist()
        .with_document_restriction(document_restriction_mock)
        .build()
    )

    assert len(result.documents) == 1
    assert result.documents[0] == document_restriction_mock


def test_should_accept_multiple_document_restrictions():
    document_restriction_mock = Mock(spec=DocumentRestriction)
    other_document_restriction_mock = Mock(spec=DocumentRestriction)

    result = (
        DocumentRestrictionsFilterBuilder()
        .for_whitelist()
        .with_document_restriction(document_restriction_mock)
        .with_document_restriction(other_document_restriction_mock)
        .build()
    )

    assert len(result.documents) == 2


def test_to_json_should_not_throw_exception():
    document_restriction_mock = Mock(spec=DocumentRestriction)
    document_restriction_mock.to_json.return_value = {}

    result = (
        DocumentRestrictionsFilterBuilder()
        .for_whitelist()
        .with_document_restriction(document_restriction_mock)
        .build()
    )

    s = json.dumps(result, cls=YotiEncoder)
    assert s is not None and s != ""
