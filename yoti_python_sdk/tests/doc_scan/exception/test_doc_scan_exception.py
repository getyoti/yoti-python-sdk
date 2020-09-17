import json

from yoti_python_sdk.doc_scan.exception import DocScanException
from yoti_python_sdk.tests.mocks import MockResponse


def test_return_message():
    response = MockResponse(status_code=400, text="some response")
    exception = DocScanException("some error", response)

    assert exception.message == "some error"


def test_return_only_message_when_html_response():
    response = MockResponse(
        status_code=400,
        text="<html>some html</html>",
        headers={"Content-Type": "text/html"},
    )
    exception = DocScanException("some error", response)

    assert exception.message == "some error"


def test_return_only_message_when_json_response_has_no_message_property():
    response = MockResponse(
        status_code=400,
        text=json.dumps({}),
        headers={"Content-Type": "application/json"},
    )
    exception = DocScanException("some error", response)

    assert exception.message == "some error"


def test_return_formatted_response_code_and_message():
    response = MockResponse(
        status_code=400,
        text=json.dumps({"code": "SOME_CODE", "message": "some message"}),
        headers={"Content-Type": "application/json"},
    )
    exception = DocScanException("some error", response)

    assert exception.message == "some error - SOME_CODE - some message"


def test_return_formatted_response_code_message_and_errors():
    response = MockResponse(
        status_code=400,
        text=json.dumps(
            {
                "code": "SOME_CODE",
                "message": "some message",
                "errors": [
                    {"property": "some.property", "message": "some message"},
                    {
                        "property": "some.other.property",
                        "message": "some other message",
                    },
                ],
            }
        ),
        headers={"Content-Type": "application/json"},
    )
    exception = DocScanException("some error", response)

    assert (
        exception.message
        == 'some error - SOME_CODE - some message: some.property "some message", some.other.property "some other message"'
    )


def test_excludes_errors_without_property_or_message():
    response = MockResponse(
        status_code=400,
        text=json.dumps(
            {
                "code": "SOME_CODE",
                "message": "some message",
                "errors": [
                    {"message": "some message"},
                    {"property": "some.other.property"},
                ],
            }
        ),
        headers={"Content-Type": "application/json"},
    )
    exception = DocScanException("some error", response)

    assert exception.message == "some error - SOME_CODE - some message"
