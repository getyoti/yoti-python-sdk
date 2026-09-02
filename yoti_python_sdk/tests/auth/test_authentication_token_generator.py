try:
    from unittest import mock
except ImportError:
    import mock

import base64
import json

import pytest

from yoti_python_sdk.auth import AuthenticationTokenGenerator, AuthException
from yoti_python_sdk.auth.authentication_token_generator import DEFAULT_AUTH_API_URL
from yoti_python_sdk.crypto import Crypto
from yoti_python_sdk.tests import conftest
from yoti_python_sdk.tests.mocks import MockResponse

YOTI_CLIENT_SDK_ID = "737204aa-d54e-49a4-8bde-26ddbe6d880c"


def _base64url_decode(data):
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def mocked_requests_post_auth_token(*args, **kwargs):
    body = json.dumps(
        {
            "access_token": "someAccessToken",
            "token_type": "Bearer",
            "expires_in": 3600,
            "scope": "docscan.session.create",
        }
    )
    return MockResponse(
        status_code=200, text=body, headers={"Content-Type": "application/json"}
    )


def mocked_requests_post_auth_token_error(*args, **kwargs):
    body = json.dumps(
        {"error": "invalid_scope", "error_description": "Unknown scope requested"}
    )
    return MockResponse(
        status_code=400, text=body, headers={"Content-Type": "application/json"}
    )


@pytest.fixture(scope="module")
def crypto():
    return Crypto.read_pem_file(conftest.PEM_FILE_PATH)


@pytest.fixture
def generator(crypto):
    return (
        AuthenticationTokenGenerator.builder()
        .with_sdk_id(YOTI_CLIENT_SDK_ID)
        .with_pem_file(crypto)
        .build()
    )


class TestAuthenticationTokenGeneratorBuilder(object):
    def test_builder_requires_sdk_id(self, crypto):
        with pytest.raises(ValueError) as ex:
            AuthenticationTokenGenerator.builder().with_pem_file(crypto).build()

        assert "sdk_id" in str(ex.value)

    def test_builder_requires_pem_file(self):
        with pytest.raises(ValueError) as ex:
            (
                AuthenticationTokenGenerator.builder()
                .with_sdk_id(YOTI_CLIENT_SDK_ID)
                .build()
            )

        assert "pem_file" in str(ex.value)

    def test_builder_accepts_pem_file_path(self):
        result = (
            AuthenticationTokenGenerator.builder()
            .with_sdk_id(YOTI_CLIENT_SDK_ID)
            .with_pem_file(conftest.PEM_FILE_PATH)
            .build()
        )

        assert isinstance(result, AuthenticationTokenGenerator)

    def test_builder_uses_default_auth_api_url(self, crypto):
        result = (
            AuthenticationTokenGenerator.builder()
            .with_sdk_id(YOTI_CLIENT_SDK_ID)
            .with_pem_file(crypto)
            .build()
        )

        assert (
            result._AuthenticationTokenGenerator__auth_api_url  # noqa
            == DEFAULT_AUTH_API_URL
        )

    def test_builder_with_auth_api_url_override(self, crypto):
        result = (
            AuthenticationTokenGenerator.builder()
            .with_sdk_id(YOTI_CLIENT_SDK_ID)
            .with_pem_file(crypto)
            .with_auth_api_url("https://example.com/oauth/token")
            .build()
        )

        assert (
            result._AuthenticationTokenGenerator__auth_api_url  # noqa
            == "https://example.com/oauth/token"
        )


class TestAuthenticationTokenGenerator(object):
    def test_generate_raises_for_empty_scopes(self, generator):
        with pytest.raises(ValueError) as ex:
            generator.generate([])

        assert "scopes must not be empty" in str(ex.value)

    @mock.patch("requests.post", side_effect=mocked_requests_post_auth_token)
    def test_generate_returns_token_response(self, mock_post, generator):
        response = generator.generate(["docscan.session.create"])

        assert response.access_token == "someAccessToken"
        assert response.token_type == "Bearer"
        assert response.expires_in == 3600
        assert response.scope == "docscan.session.create"
        mock_post.assert_called_once()

    @mock.patch("requests.post", side_effect=mocked_requests_post_auth_token)
    def test_generate_sends_signed_jwt_client_assertion(self, mock_post, generator):
        generator.generate(["docscan.session.create"])

        _, kwargs = mock_post.call_args
        form_data = kwargs["data"]

        assert form_data["grant_type"] == "client_credentials"
        assert (
            form_data["client_assertion_type"]
            == "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"
        )
        assert form_data["scope"] == "docscan.session.create"

        jwt = form_data["client_assertion"]
        header_b64, payload_b64, _signature_b64 = jwt.split(".")
        header = json.loads(_base64url_decode(header_b64))
        payload = json.loads(_base64url_decode(payload_b64))

        assert header == {"alg": "PS384", "typ": "JWT"}
        assert payload["iss"] == "sdk:" + YOTI_CLIENT_SDK_ID
        assert payload["sub"] == "sdk:" + YOTI_CLIENT_SDK_ID
        assert payload["aud"] == DEFAULT_AUTH_API_URL
        assert payload["exp"] - payload["iat"] == 300

    @mock.patch("requests.post", side_effect=mocked_requests_post_auth_token_error)
    def test_generate_raises_auth_exception_on_error(self, mock_post, generator):
        with pytest.raises(AuthException) as ex:
            generator.generate(["docscan.session.create"])

        assert "Failed to generate authentication token" in str(ex.value)
        assert "invalid_scope - Unknown scope requested" in str(ex.value)
        assert ex.value.status_code == 400
