# -*- coding: utf-8 -*-
import re

import pytest

from yoti_python_sdk.auth_strategy import (
    BearerTokenStrategy,
    NoAuthStrategy,
    SignedRequestStrategy,
)
from yoti_python_sdk.crypto import Crypto
from yoti_python_sdk.tests import conftest


@pytest.fixture(scope="module")
def crypto():
    return Crypto.read_pem_file(conftest.PEM_FILE_PATH)


class TestSignedRequestStrategy(object):
    def test_create_auth_headers_returns_digest(self, crypto):
        strategy = SignedRequestStrategy(crypto)

        headers = strategy.create_auth_headers("GET", "/profile", None)

        assert "X-Yoti-Auth-Digest" in headers

    def test_create_auth_headers_with_payload_returns_digest(self, crypto):
        strategy = SignedRequestStrategy(crypto)

        headers = strategy.create_auth_headers("POST", "/profile", b"some-payload")

        assert "X-Yoti-Auth-Digest" in headers

    def test_create_query_params_returns_nonce_and_timestamp(self, crypto):
        strategy = SignedRequestStrategy(crypto)

        query_params = strategy.create_query_params()

        assert "nonce" in query_params
        assert re.match(
            r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
            str(query_params["nonce"]),
        )
        assert "timestamp" in query_params

    def test_create_query_params_returns_different_nonces(self, crypto):
        strategy = SignedRequestStrategy(crypto)

        first = strategy.create_query_params()
        second = strategy.create_query_params()

        assert first["nonce"] != second["nonce"]


class TestBearerTokenStrategy(object):
    def test_create_auth_headers_returns_authorization_header(self):
        strategy = BearerTokenStrategy("someAuthToken")

        headers = strategy.create_auth_headers("GET", "/profile", None)

        assert headers == {"Authorization": "Bearer someAuthToken"}

    def test_create_query_params_returns_empty_dict(self):
        strategy = BearerTokenStrategy("someAuthToken")

        assert strategy.create_query_params() == {}

    def test_raises_for_none_token(self):
        with pytest.raises(ValueError) as ex:
            BearerTokenStrategy(None)

        assert "auth_token must not be empty" in str(ex.value)

    def test_raises_for_empty_token(self):
        with pytest.raises(ValueError) as ex:
            BearerTokenStrategy("")

        assert "auth_token must not be empty" in str(ex.value)


class TestNoAuthStrategy(object):
    def test_create_auth_headers_returns_empty_dict(self):
        strategy = NoAuthStrategy()

        assert strategy.create_auth_headers("GET", "/profile", None) == {}

    def test_create_query_params_returns_empty_dict(self):
        strategy = NoAuthStrategy()

        assert strategy.create_query_params() == {}
