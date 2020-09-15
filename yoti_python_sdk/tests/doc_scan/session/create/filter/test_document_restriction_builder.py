import json

from yoti_python_sdk.doc_scan.session.create.filter import DocumentRestrictionBuilder
from yoti_python_sdk.utils import YotiEncoder


def test_should_build_without_setting_properties():
    result = DocumentRestrictionBuilder().build()

    assert result.document_types is None
    assert result.country_codes is None


def test_with_country_codes():
    result = (
        DocumentRestrictionBuilder().with_country_codes(["GBR", "USA", "UKR"]).build()
    )

    assert len(result.country_codes) == 3
    assert result.country_codes == ["GBR", "USA", "UKR"]


def test_with_document_types():
    result = (
        DocumentRestrictionBuilder()
        .with_document_types(["PASSPORT", "DRIVING_LICENCE"])
        .build()
    )

    assert len(result.document_types) == 2
    assert result.document_types == ["PASSPORT", "DRIVING_LICENCE"]


def test_to_json_should_not_throw_exception():
    result = (
        DocumentRestrictionBuilder()
        .with_country_codes(["GBR", "USA", "UKR"])
        .with_document_types(["PASSPORT", "DRIVING_LICENCE"])
        .build()
    )

    s = json.dumps(result, cls=YotiEncoder)
    assert s is not None and s != ""


def test_to_json_should_not_include_null_values():
    result = (
        DocumentRestrictionBuilder()
        .with_document_types(["PASSPORT", "DRIVING_LICENCE"])
        .build()
    )

    s = json.dumps(result, cls=YotiEncoder)
    assert s is not None
    assert "null" not in s
