import json
import unittest

from yoti_python_sdk.doc_scan.session.create.company_profile import CompanyProfile
from yoti_python_sdk.utils import YotiEncoder


class CompanyProfileTest(unittest.TestCase):
    SOME_COMPANY_NAME = "Some Company Ltd"

    def test_should_store_company_name(self):
        result = CompanyProfile(self.SOME_COMPANY_NAME)

        assert result.company_name == self.SOME_COMPANY_NAME

    def test_should_serialize_company_name_to_json(self):
        result = CompanyProfile(self.SOME_COMPANY_NAME)

        serialized = json.dumps(result, cls=YotiEncoder)
        parsed = json.loads(serialized)

        assert parsed["company_name"] == self.SOME_COMPANY_NAME

    def test_should_omit_null_company_name_from_json(self):
        result = CompanyProfile(None)

        serialized = json.dumps(result, cls=YotiEncoder)
        parsed = json.loads(serialized)

        assert "company_name" not in parsed


if __name__ == "__main__":
    unittest.main()
