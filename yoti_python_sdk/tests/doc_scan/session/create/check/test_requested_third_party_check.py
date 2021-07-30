import json
import unittest

from yoti_python_sdk.doc_scan import constants
from yoti_python_sdk.doc_scan.session.create.check import (
    RequestedThirdPartyCheckBuilder,
)
from yoti_python_sdk.doc_scan.session.create.check.requested_check import RequestedCheck
from yoti_python_sdk.doc_scan.session.create.check.third_party import (
    RequestedThirdPartyCheck,
    RequestedThirdPartyCheckConfig,
)
from yoti_python_sdk.utils import YotiEncoder


class RequestedThirdPartyCheckTest(unittest.TestCase):
    def test_should_build_correctly(self):
        dummy_manual_check = "DUMMY_MANUAL_TYPE"

        result = (
            RequestedThirdPartyCheckBuilder()
            .with_manual_check(dummy_manual_check)
            .build()
        )

        assert isinstance(result, RequestedCheck)
        assert isinstance(result, RequestedThirdPartyCheck)

        assert result.type == constants.THIRD_PARTY_IDENTITY
        assert result.config.manual_check == dummy_manual_check

    def test_should_serialize_to_json_without_error(self):
        another_dummy_manual_check = "DUMMY_MANUAL_TYPE"

        result = (
            RequestedThirdPartyCheckBuilder()
            .with_manual_check(another_dummy_manual_check)
            .build()
        )

        s = json.dumps(result, cls=YotiEncoder)
        assert s is not None and s != ""


if _name_ == "_main_":
    unittest.main()
