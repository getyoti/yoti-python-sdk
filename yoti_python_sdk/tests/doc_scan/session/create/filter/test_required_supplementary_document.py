import json
import unittest

from mock import (
    Mock,
    MagicMock,
)

from yoti_python_sdk.doc_scan.session.create.objective.objective import Objective
from yoti_python_sdk.doc_scan.session.create.objective import (
    ProofOfAddressObjectiveBuilder,
)
from yoti_python_sdk.doc_scan.session.create.filter.required_document import (
    RequiredDocument,
)
from yoti_python_sdk.doc_scan.session.create.filter.required_supplementary_document import (
    RequiredSupplementaryDocument,
    RequiredSupplementaryDocumentBuilder,
)
from yoti_python_sdk.utils import YotiEncoder


class RequestedSupplementaryDocTextExtractionTaskTest(unittest.TestCase):
    def test_builds_required_supplementary_document(self):
        objective_mock = Mock(spec=Objective)

        result = (
            RequiredSupplementaryDocumentBuilder()
            .with_objective(objective_mock)
            .build()
        )

        assert isinstance(result, RequiredDocument)
        assert isinstance(result, RequiredSupplementaryDocument)
        assert result.type == "SUPPLEMENTARY_DOCUMENT"

    def test_to_json_contains_proof_of_address_objective(self):
        proof_of_address_objective = ProofOfAddressObjectiveBuilder().build()

        result = (
            RequiredSupplementaryDocumentBuilder()
            .with_objective(proof_of_address_objective)
            .build()
        )

        assert result.to_json().get("objective") == proof_of_address_objective

    def test_to_json_contains_country_codes(self):
        objective_mock = Mock(spec=Objective)
        some_country_codes = ["GBR", "USA"]

        result = (
            RequiredSupplementaryDocumentBuilder()
            .with_objective(objective_mock)
            .with_country_codes(some_country_codes)
            .build()
        )

        assert result.to_json().get("country_codes") == some_country_codes

    def test_to_json_contains_document_types(self):
        objective_mock = Mock(spec=Objective)
        some_document_types = ["UTILITY_BILL"]

        result = (
            RequiredSupplementaryDocumentBuilder()
            .with_objective(objective_mock)
            .with_document_types(some_document_types)
            .build()
        )

        assert result.to_json().get("document_types") == some_document_types

    def test_to_json_excludes_none_values(self):
        objective_mock = Mock(spec=Objective)

        result = (
            RequiredSupplementaryDocumentBuilder()
            .with_objective(objective_mock)
            .build()
        )

        assert "country_codes" not in result.to_json().keys()
        assert "document_types" not in result.to_json().keys()

    def test_should_serialize_to_json_without_error(self):
        objective_mock = Mock(spec=Objective)
        objective_mock.to_json = MagicMock(return_value="")

        result = (
            RequiredSupplementaryDocumentBuilder()
            .with_objective(objective_mock)
            .build()
        )

        s = json.dumps(result, cls=YotiEncoder)
        assert s is not None and s != ""
