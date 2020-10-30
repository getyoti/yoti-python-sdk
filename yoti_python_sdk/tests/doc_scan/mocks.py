from os.path import abspath
from os.path import dirname
from os.path import join

from yoti_python_sdk.tests.mocks import MockResponse

FIXTURES_DIR = join(dirname(abspath(__file__)), "fixtures")


def mocked_request_successful_session_creation():
    with open(FIXTURES_DIR + "/session_create_success.txt", "r") as f:
        response = f.read()
    return MockResponse(status_code=201, text=response)


def mocked_request_failed_session_creation():
    with open(FIXTURES_DIR + "/failed_request.txt", "r") as f:
        response = f.read()
    return MockResponse(status_code=400, text=response)


def mocked_request_successful_session_retrieval():
    with open(FIXTURES_DIR + "/retrieve_session_success.txt", "r") as f:
        response = f.read()
    return MockResponse(status_code=200, text=response)


def mocked_request_failed_session_retrieval():
    return MockResponse(status_code=400, text="")


def mocked_request_media_content():
    return MockResponse(
        status_code=200,
        text="someContent",
        content=b"someContent",
        headers={"Content-Type": "application/json"},
    )


def mocked_request_no_content():
    return MockResponse(status_code=204, text="")


def mocked_request_not_found():
    return MockResponse(status_code=404, text="")


def mocked_supported_documents_content():
    with open(FIXTURES_DIR + "/supported_documents_success.txt", "r") as f:
        response = f.read()
    return MockResponse(status_code=200, text=response)


def mocked_request_server_error():
    return MockResponse(status_code=500, text="")
