import json

from yoti_python_sdk.doc_scan.session.create.filter import (
    OrthogonalRestrictionsFilterBuilder,
)
from yoti_python_sdk.doc_scan.session.create.filter.orthogonal_restrictions_filter import (
    CountryRestriction,
    TypeRestriction,
)
from yoti_python_sdk.utils import YotiEncoder


def test_should_create_correct_country_restriction():
    result = (
        OrthogonalRestrictionsFilterBuilder()
        .with_whitelisted_country_codes(["GBR", "USA"])
        .build()
    )

    assert isinstance(result.country_restriction, CountryRestriction)
    assert result.country_restriction.inclusion == "WHITELIST"
    assert result.country_restriction.country_codes == ["GBR", "USA"]


def test_should_create_correct_type_restriction():
    result = (
        OrthogonalRestrictionsFilterBuilder()
        .with_whitelisted_document_types(["PASSPORT", "DRIVING_LICENCE"])
        .build()
    )

    assert isinstance(result.type_restriction, TypeRestriction)
    assert result.type_restriction.inclusion == "WHITELIST"
    assert result.type_restriction.document_types == ["PASSPORT", "DRIVING_LICENCE"]


def test_should_set_inclusion_to_whitelist():
    result = (
        OrthogonalRestrictionsFilterBuilder()
        .with_whitelisted_document_types([])
        .with_whitelisted_country_codes([])
        .build()
    )

    assert result.country_restriction.inclusion == "WHITELIST"
    assert result.type_restriction.inclusion == "WHITELIST"


def test_should_set_inclusion_to_blacklist():
    result = (
        OrthogonalRestrictionsFilterBuilder()
        .with_blacklisted_country_codes([])
        .with_blacklisted_document_types([])
        .build()
    )

    assert result.country_restriction.inclusion == "BLACKLIST"
    assert result.type_restriction.inclusion == "BLACKLIST"


def test_to_json_should_not_throw_exception():
    result = (
        OrthogonalRestrictionsFilterBuilder()
        .with_whitelisted_document_types(["PASSPORT", "DRIVING_LICENCE"])
        .with_whitelisted_country_codes(["GBR", "USA", "UKR"])
        .build()
    )

    s = json.dumps(result, cls=YotiEncoder)
    assert s is not None and s != ""
