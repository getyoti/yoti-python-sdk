import json
import unittest

from yoti_python_sdk.doc_scan.session.create.objective.objective import Objective
from yoti_python_sdk.doc_scan.session.create.objective.proof_of_address_objective import (
    ProofOfAddressObjective,
)
from yoti_python_sdk.doc_scan.session.create.objective import (
    ProofOfAddressObjectiveBuilder,
)
from yoti_python_sdk.utils import YotiEncoder


class ProofOfAddressObjectiveTest(unittest.TestCase):
    def test_builder_builds_proof_of_address_objective(self):
        result = ProofOfAddressObjectiveBuilder().build()

        assert isinstance(result, Objective)
        assert isinstance(result, ProofOfAddressObjective)
        assert result.type == "PROOF_OF_ADDRESS"

    def test_to_json_contains_type(self):
        result = ProofOfAddressObjectiveBuilder().build()

        assert result.to_json().get("type") == "PROOF_OF_ADDRESS"

    def test_should_serialize_to_json_without_error(self):
        result = ProofOfAddressObjectiveBuilder().build()

        s = json.dumps(result, cls=YotiEncoder)
        assert s is not None and s != ""
