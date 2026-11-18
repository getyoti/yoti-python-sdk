import unittest

from yoti_python_sdk.doc_scan.session.create.filter.orthogonal_restrictions_filter import \
    OrthogonalRestrictionsFilterBuilder
from yoti_python_sdk.doc_scan.session.create.subcheck import (
    IssuingAuthoritySubCheckBuilder
)
from yoti_python_sdk.doc_scan.session.create.subcheck.issuing_authority_sub_check import IssuingAuthoritySubCheck


class IssuingAuthoritySubCheckTest(unittest.TestCase):
    def test_should_build_correctly_without_additional_data(self):
        issuing_authority_sub_check = IssuingAuthoritySubCheckBuilder().build()

        assert isinstance(issuing_authority_sub_check, IssuingAuthoritySubCheck)

    def test_should_build_correctly_with_filter(self):
        filter = OrthogonalRestrictionsFilterBuilder().with_whitelisted_country_codes(
            ["GBR", "FRA"]).with_whitelisted_document_types(["PASSPORT", "STATE_ID"]).build()

        issuing_authority_sub_check = IssuingAuthoritySubCheckBuilder().with_filter(
            filter=filter).build()

        assert isinstance(issuing_authority_sub_check, IssuingAuthoritySubCheck)
        assert issuing_authority_sub_check.filter == filter

    def test_should_always_build_with_requested_as_boolean_true(self):
        issuing_authority_sub_check = IssuingAuthoritySubCheckBuilder().build()

        assert issuing_authority_sub_check.requested is True

    def test_allow_non_latin_documents_set_to_true(self):
        filter = OrthogonalRestrictionsFilterBuilder().allow_non_latin_documents().build()

        assert filter.allow_non_latin_documents is True

    def test_allow_non_latin_documents_set_to_false(self):
        filter = OrthogonalRestrictionsFilterBuilder().disable_non_latin_documents().build()

        assert filter.allow_non_latin_documents is False

    def test_default_non_latin_documents(self):
        filter = OrthogonalRestrictionsFilterBuilder().build()

        assert 'allow_non_latin_documents' not in filter.to_json()

    def test_build_invalid_filter(self):
        filter = 'invalid'

        with self.assertRaises(ValueError):
            IssuingAuthoritySubCheckBuilder().with_filter(
                filter=filter).build()


if __name__ == "__main__":
    unittest.main()
