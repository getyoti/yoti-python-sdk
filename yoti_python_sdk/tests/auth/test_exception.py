import json

from yoti_python_sdk.auth.exception import AuthException
from yoti_python_sdk.tests.mocks import MockResponse


def test_return_message():
    response = MockResponse(status_code=400, text="some response")
    exception = AuthException("some error", response)

    assert exception.message == "some error"


def test_return_only_message_when_html_response():
    response = MockResponse(
        status_code=400,
        text="<html>some html</html>",
        headers={"Content-Type": "text/html"},
    )
    exception = AuthException("some error", response)

    assert exception.message == "some error"


def test_return_only_message_when_json_response_has_no_error_property():
    response = MockResponse(
        status_code=400,
        text=json.dumps({}),
        headers={"Content-Type": "application/json"},
    )
    exception = AuthException("some error", response)

    assert exception.message == "some error"


def test_return_formatted_error_without_description():
    response = MockResponse(
        status_code=400,
        text=json.dumps({"error": "invalid_scope"}),
        headers={"Content-Type": "application/json"},
    )
    exception = AuthException("some error", response)

    assert exception.message == "some error - invalid_scope"


def test_return_formatted_error_and_description():
    response = MockResponse(
        status_code=400,
        text=json.dumps(
            {"error": "invalid_scope", "error_description": "Unknown scope requested"}
        ),
        headers={"Content-Type": "application/json"},
    )
    exception = AuthException("some error", response)

    assert exception.message == "some error - invalid_scope - Unknown scope requested"


def test_status_code_and_text_properties():
    response = MockResponse(status_code=400, text="some response")
    exception = AuthException("some error", response)

    assert exception.status_code == 400
    assert exception.text == "some response"


def test_str_returns_message():
    response = MockResponse(status_code=400, text="some response")
    exception = AuthException("some error", response)

    assert str(exception) == "some error"
