from yoti_python_sdk.doc_scan.support.supported_documents import (
    SupportedCountry,
    SupportedDocument,
    SupportedDocumentsResponse,
)


def test_supported_document_should_parse_data():
    data = {"type": "someSupportedDocument"}

    result = SupportedDocument(data)

    assert result.type == "someSupportedDocument"


def test_supported_document_should_not_throw_exception_on_missing_data():
    result = SupportedDocument(None)
    assert result.type is None


def test_supported_document_created_with_is_strictly_latin_as_true():
    result = SupportedDocument({"is_strictly_latin": True})

    assert result.is_strictly_latin is True


def test_supported_document_created_with_is_strictly_latin_as_false():
    result = SupportedDocument({"is_strictly_latin": False})

    assert result.is_strictly_latin is False


def test_supported_document_created_without_is_strictly_latin():
    result = SupportedDocument({"type": "someSupportedDocument"})

    assert result.is_strictly_latin is None


def test_supported_country_should_parse_data():
    data = {
        "code": "someCode",
        "supported_documents": [{"type": "firstType"}, {"type": "secondType"}],
    }

    result = SupportedCountry(data)

    assert result.code == "someCode"
    assert len(result.supported_documents) == 2


def test_supported_country_should_not_throw_exception_on_missing_data():
    result = SupportedCountry(None)

    assert result.code is None
    assert len(result.supported_documents) == 0


def test_supported_document_response_should_parse_data():
    data = {"supported_countries": [{"code": "GBR"}, {"code": "USA"}]}

    result = SupportedDocumentsResponse(data)

    assert len(result.supported_countries) == 2


def test_supported_document_response_should_not_throw_exception_on_missing_data():
    result = SupportedDocumentsResponse(None)

    assert len(result.supported_countries) == 0
