from yoti_python_sandbox.client import SandboxClient
from yoti_python_sandbox.token import YotiTokenRequest, YotiTokenResponse
from yoti_python_sdk.tests.conftest import PEM_FILE_PATH

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

import pytest


def test_builder_should_throw_error_for_missing_sdk_id():
    builder = SandboxClient.builder().with_pem_file("some_pem.pem")
    with pytest.raises(ValueError):
        builder.build()


def test_builder_should_throw_error_for_missing_pem_file():
    builder = SandboxClient.builder().for_application("my_application")
    with pytest.raises(ValueError):
        builder.build()


def test_builder_should_build_client():
    client = (
        SandboxClient.builder()
        .for_application("some_app")
        .with_pem_file(PEM_FILE_PATH)
        .with_sandbox_url("https://localhost")
        .build()
    )

    assert client.sdk_id == "some_app"
    assert isinstance(client, SandboxClient)


@patch("yoti_python_sandbox.client.SandboxClient")
def test_client_should_return_token_from_sandbox(sandbox_client_mock):
    sandbox_client_mock.setup_profile_share.return_value = YotiTokenResponse(
        "some-token"
    )

    token_request = (
        YotiTokenRequest.builder().with_remember_me_id("remember_me_pls").build()
    )
    response = sandbox_client_mock.setup_profile_share(token_request)

    assert response.token == "some-token"
