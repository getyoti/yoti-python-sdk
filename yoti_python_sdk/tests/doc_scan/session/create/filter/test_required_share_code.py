import json
import unittest

from yoti_python_sdk.doc_scan.session.create.filter.required_share_code import (
    RequiredShareCode,
    RequiredShareCodeBuilder,
)
from yoti_python_sdk.utils import YotiEncoder


class RequiredShareCodeTest(unittest.TestCase):
    SOME_ISSUER = "some-issuer"
    SOME_SCHEME = "some-scheme"

    def test_should_build_correctly_with_issuer_and_scheme(self):
        result = (
            RequiredShareCodeBuilder()
            .with_issuer(self.SOME_ISSUER)
            .with_scheme(self.SOME_SCHEME)
            .build()
        )

        assert result.issuer == self.SOME_ISSUER
        assert result.scheme == self.SOME_SCHEME

    def test_should_build_correctly_with_only_issuer(self):
        result = RequiredShareCodeBuilder().with_issuer(self.SOME_ISSUER).build()

        assert result.issuer == self.SOME_ISSUER
        assert result.scheme is None

    def test_should_build_correctly_with_only_scheme(self):
        result = RequiredShareCodeBuilder().with_scheme(self.SOME_SCHEME).build()

        assert result.issuer is None
        assert result.scheme == self.SOME_SCHEME

    def test_should_build_correctly_with_no_fields(self):
        result = RequiredShareCodeBuilder().build()

        assert result.issuer is None
        assert result.scheme is None

    def test_should_serialize_to_json_without_error(self):
        result = (
            RequiredShareCodeBuilder()
            .with_issuer(self.SOME_ISSUER)
            .with_scheme(self.SOME_SCHEME)
            .build()
        )

        s = json.dumps(result, cls=YotiEncoder)
        assert s is not None and s != ""

        parsed = json.loads(s)
        assert parsed["issuer"] == self.SOME_ISSUER
        assert parsed["scheme"] == self.SOME_SCHEME

    def test_should_not_include_null_values_in_json(self):
        result = RequiredShareCodeBuilder().with_issuer(self.SOME_ISSUER).build()

        s = json.dumps(result, cls=YotiEncoder)
        parsed = json.loads(s)

        assert parsed["issuer"] == self.SOME_ISSUER
        assert "scheme" not in parsed

    def test_should_create_directly(self):
        result = RequiredShareCode(issuer=self.SOME_ISSUER, scheme=self.SOME_SCHEME)

        assert result.issuer == self.SOME_ISSUER
        assert result.scheme == self.SOME_SCHEME


if __name__ == "__main__":
    unittest.main()
