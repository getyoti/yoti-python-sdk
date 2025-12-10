import json
import unittest

from yoti_python_sdk.doc_scan.session.create.filter.required_share_code import (
    RequiredShareCode,
    RequiredShareCodeBuilder,
)
from yoti_python_sdk.utils import YotiEncoder


class RequiredShareCodeTest(unittest.TestCase):
    SOME_ISSUER = "someIssuer"
    SOME_SCHEME = "someScheme"

    def test_should_build_correctly(self):
        result = (
            RequiredShareCodeBuilder()
            .with_issuer(self.SOME_ISSUER)
            .with_scheme(self.SOME_SCHEME)
            .build()
        )

        assert result.issuer == self.SOME_ISSUER
        assert result.scheme == self.SOME_SCHEME
        assert result.type == "SHARE_CODE"

    def test_should_serialize_to_json_without_error(self):
        result = (
            RequiredShareCodeBuilder()
            .with_issuer(self.SOME_ISSUER)
            .with_scheme(self.SOME_SCHEME)
            .build()
        )

        s = json.dumps(result, cls=YotiEncoder)
        assert s is not None and s != ""

        json_data = json.loads(s)
        assert json_data["issuer"] == self.SOME_ISSUER
        assert json_data["scheme"] == self.SOME_SCHEME

    def test_should_handle_none_values(self):
        result = RequiredShareCodeBuilder().build()

        assert result.issuer is None
        assert result.scheme is None
        assert result.type == "SHARE_CODE"

    def test_should_not_include_null_values_in_json(self):
        result = RequiredShareCodeBuilder().build()

        json_data = result.to_json()
        assert "issuer" not in json_data
        assert "scheme" not in json_data


if __name__ == "__main__":
    unittest.main()
