import json
import unittest

from yoti_python_sdk.doc_scan.session.create.check.third_party_identity import (
    RequestedThirdPartyIdentityCheck,
    RequestedThirdPartyIdentityCheckConfig,
    RequestedThirdPartyIdentityCheckBuilder,
)
from yoti_python_sdk.doc_scan.session.create.check.requested_check import RequestedCheck
from yoti_python_sdk.utils import YotiEncoder


class RequestedThirdPartyIdentityCheckTest(unittest.TestCase):
    def test_should_build_correctly(self):
        result = RequestedThirdPartyIdentityCheckBuilder().build()

        assert isinstance(result, RequestedCheck)
        assert isinstance(result, RequestedThirdPartyIdentityCheck)
        assert isinstance(result.config, RequestedThirdPartyIdentityCheckConfig)
        assert result.type == "THIRD_PARTY_IDENTITY"

    def test_should_serialize_to_json_without_error(self):
        result = RequestedThirdPartyIdentityCheckBuilder().build()

        s = json.dumps(result, cls=YotiEncoder)
        assert s is not None and s != ""


if __name__ == "__main__":
    unittest.main()
