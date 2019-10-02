try:
    from unittest import mock
except ImportError:
    import mock

from yoti_python_sdk.http import SignedRequest, DefaultRequestHandler
from yoti_python_sdk.crypto import Crypto
from yoti_python_sdk.tests import conftest

from yoti_python_sdk.tests.mocks import mocked_requests_get

import pytest
import json


@pytest.fixture(scope="module")
def json_payload():
    payload = {"Hello": "World"}
    return json.dumps(payload).encode()


@pytest.fixture(scope="module")
def valid_base_url():
    return "https://localhost:8443/api/v1"


@pytest.fixture(scope="module")
def valid_endpoint():
    return "/profile"


@pytest.fixture(scope="module")
def expected_request_headers():
    return ["X-Yoti-Auth-Digest", "X-Yoti-SDK", "X-Yoti-SDK-Version"]


def test_create_signed_request_get_required_properties(
    valid_base_url, valid_endpoint, expected_request_headers
):
    http_method = "GET"

    signed_request = (
        SignedRequest.builder()
        .with_pem_file(conftest.PEM_FILE_PATH)
        .with_base_url(valid_base_url)
        .with_endpoint(valid_endpoint)
        .with_http_method(http_method)
        .build()
    )

    assert (valid_base_url + valid_endpoint) in signed_request.url
    assert signed_request.method == http_method
    assert signed_request.data is None

    header_keys = signed_request.headers.keys()
    for header in expected_request_headers:
        assert header in header_keys


def test_create_signed_request_missing_pem_file(valid_base_url, valid_endpoint):
    http_method = "GET"

    with pytest.raises(ValueError) as ex:
        (
            SignedRequest.builder()
            .with_base_url(valid_base_url)
            .with_endpoint(valid_endpoint)
            .with_http_method(http_method)
            .build()
        )

    assert "PEM file" in str(ex.value)


def test_create_signed_request_missing_base_url(valid_endpoint):
    http_method = "GET"

    with pytest.raises(ValueError) as ex:
        (
            SignedRequest.builder()
            .with_pem_file(conftest.PEM_FILE_PATH)
            .with_endpoint(valid_endpoint)
            .with_http_method(http_method)
            .build()
        )

    assert "Base URL" in str(ex.value)


def test_create_signed_request_missing_endpoint(valid_base_url):
    http_method = "GET"

    with pytest.raises(ValueError) as ex:
        (
            SignedRequest.builder()
            .with_pem_file(conftest.PEM_FILE_PATH)
            .with_base_url(valid_base_url)
            .with_http_method(http_method)
            .build()
        )

    assert "Endpoint" in str(ex.value)


def test_create_signed_request_missing_http_method(valid_base_url, valid_endpoint):
    with pytest.raises(ValueError) as ex:
        (
            SignedRequest.builder()
            .with_pem_file(conftest.PEM_FILE_PATH)
            .with_base_url(valid_base_url)
            .with_endpoint(valid_endpoint)
            .build()
        )

    assert "HTTP method" in str(ex.value)


def test_create_signed_request_with_invalid_http_method():

    with pytest.raises(ValueError) as ex:
        SignedRequest.builder().with_http_method("INVALID").build()

    assert str(ex.value) == "INVALID is an unsupported HTTP method"


def test_create_signed_request_with_payload(
    valid_base_url, valid_endpoint, json_payload
):
    http_method = "POST"

    signed_request = (
        SignedRequest.builder()
        .with_pem_file(conftest.PEM_FILE_PATH)
        .with_base_url(valid_base_url)
        .with_endpoint(valid_endpoint)
        .with_http_method(http_method)
        .with_payload(json_payload)
        .build()
    )

    assert signed_request.data == json_payload


def test_create_signed_request_with_header(valid_base_url, valid_endpoint):
    http_method = "POST"

    signed_request = (
        SignedRequest.builder()
        .with_pem_file(conftest.PEM_FILE_PATH)
        .with_base_url(valid_base_url)
        .with_endpoint(valid_endpoint)
        .with_http_method(http_method)
        .with_header("My-Http-Header", "someValue")
        .build()
    )

    headers = signed_request.headers

    assert "My-Http-Header" in headers
    assert headers["My-Http-Header"] == "someValue"


def test_create_signed_request_with_query_param(valid_base_url, valid_endpoint):
    http_method = "POST"

    signed_request = (
        SignedRequest.builder()
        .with_pem_file(conftest.PEM_FILE_PATH)
        .with_base_url(valid_base_url)
        .with_endpoint(valid_endpoint)
        .with_http_method(http_method)
        .with_param("sdkId", "mySdkId")
        .build()
    )

    assert "sdkId=mySdkId" in signed_request.url


def test_create_signed_request_with_crypto_object(valid_base_url, valid_endpoint):
    http_method = "GET"
    crypto = Crypto.read_pem_file(conftest.PEM_FILE_PATH)

    (
        SignedRequest.builder()
        .with_pem_file(crypto)
        .with_base_url(valid_base_url)
        .with_endpoint(valid_endpoint)
        .with_http_method(http_method)
        .build()
    )


def test_create_signed_request_with_get_convenience_method(
    valid_base_url, valid_endpoint
):
    (
        SignedRequest.builder()
        .with_pem_file(conftest.PEM_FILE_PATH)
        .with_base_url(valid_base_url)
        .with_endpoint(valid_endpoint)
        .with_get()
        .build()
    )


def test_create_signed_request_with_post_convenience_method(
    valid_base_url, valid_endpoint, json_payload
):
    (
        SignedRequest.builder()
        .with_pem_file(conftest.PEM_FILE_PATH)
        .with_base_url(valid_base_url)
        .with_endpoint(valid_endpoint)
        .with_post()
        .with_payload(json_payload)
        .build()
    )


@mock.patch("requests.request", side_effect=mocked_requests_get)
def test_execute_signed_request(valid_base_url, valid_endpoint):
    signed_request = (
        SignedRequest.builder()
        .with_pem_file(conftest.PEM_FILE_PATH)
        .with_base_url(valid_base_url)
        .with_endpoint(valid_endpoint)
        .with_post()
        .build()
    )

    response = signed_request.execute()

    assert response.status_code == 200
    assert response.text is not None


def test_signed_request_with_custom_request_handler(
    valid_base_url, valid_endpoint, mock_request_handler
):
    signed_request = (
        SignedRequest.builder()
        .with_pem_file(conftest.PEM_FILE_PATH)
        .with_base_url(valid_base_url)
        .with_endpoint(valid_endpoint)
        .with_request_handler(mock_request_handler)
        .with_post()
        .build()
    )

    response = signed_request.execute()

    assert response.status_code == 200
    assert response.text is not None


@mock.patch("requests.request", side_effect=mocked_requests_get)
def test_signed_request_passing_request_handler_as_none(valid_base_url, valid_endpoint):
    signed_request = (
        SignedRequest.builder()
        .with_pem_file(conftest.PEM_FILE_PATH)
        .with_base_url(valid_base_url)
        .with_endpoint(valid_endpoint)
        .with_request_handler(None)
        .with_post()
        .build()
    )

    response = signed_request.execute()

    assert response.status_code == 200
    assert response.text is not None


def test_signed_request_should_throw_error_when_request_handler_wrong_type(
    valid_base_url, valid_endpoint
):

    with pytest.raises(TypeError) as ex:
        (
            SignedRequest.builder()
            .with_pem_file(conftest.PEM_FILE_PATH)
            .with_base_url(valid_base_url)
            .with_endpoint(valid_endpoint)
            .with_request_handler("myRequestHandler")
            .with_post()
            .build()
        )

    assert "yoti_python_sdk.http.RequestHandler" in str(ex.value)


def test_default_request_handler_should_raise_exception_when_passed_non_signed_request(
    valid_base_url, valid_endpoint
):
    with pytest.raises(TypeError) as ex:
        DefaultRequestHandler.execute("someBadValue")

    assert "RequestHandler expects instance of SignedRequest" == str(ex.value)
