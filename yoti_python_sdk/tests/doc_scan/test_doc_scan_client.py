import pytest

from yoti_python_sdk.doc_scan.client import DocScanClient  # noqa: F401
from yoti_python_sdk.doc_scan.exception import DocScanException
from yoti_python_sdk.doc_scan.session.create.session_spec import SessionSpec
from yoti_python_sdk.doc_scan.session.retrieve.create_session_result import (
    CreateSessionResult,
)
from yoti_python_sdk.doc_scan.session.retrieve.get_session_result import (
    GetSessionResult,
)
from yoti_python_sdk.tests.doc_scan.mocks import (
    mocked_request_failed_session_creation,
    mocked_request_failed_session_retrieval,
    mocked_request_media_content,
    mocked_request_no_content,
    mocked_request_not_found,
    mocked_request_server_error,
    mocked_request_successful_session_creation,
    mocked_request_successful_session_retrieval,
    mocked_supported_documents_content,
)

try:
    from unittest import mock
except ImportError:
    import mock

SOME_SESSION_ID = "someSessionId"
SOME_MEDIA_ID = "someMediaId"


@mock.patch(
    "yoti_python_sdk.http.SignedRequest.execute",
    side_effect=mocked_request_successful_session_creation,
)
def test_should_return_create_session_result(_, doc_scan_client):
    """
    :type doc_scan_client: DocScanClient
    :return:
    :rtype:
    """
    session_spec_mock = mock.Mock(spec=SessionSpec)
    session_spec_mock.to_json.return_value = {}

    create_session_result = doc_scan_client.create_session(session_spec_mock)

    assert isinstance(create_session_result, CreateSessionResult)


@mock.patch(
    "yoti_python_sdk.http.SignedRequest.execute",
    side_effect=mocked_request_failed_session_creation,
)
def test_should_raise_doc_scan_exception_for_session_creation(_, doc_scan_client):
    """
    :type doc_scan_client: DocScanClient
    """
    session_spec_mock = mock.Mock(spec=SessionSpec)
    session_spec_mock.to_json.return_value = {}

    with pytest.raises(DocScanException) as ex:
        doc_scan_client.create_session(session_spec_mock)

    assert "Failed to create session" in str(ex.value)


@mock.patch(
    "yoti_python_sdk.http.SignedRequest.execute",
    side_effect=mocked_request_successful_session_retrieval,
)
def test_should_return_get_session_result(_, doc_scan_client):
    """
    :type doc_scan_client: DocScanClient
    """
    session_result = doc_scan_client.get_session(SOME_SESSION_ID)

    assert isinstance(session_result, GetSessionResult)


@mock.patch(
    "yoti_python_sdk.http.SignedRequest.execute",
    side_effect=mocked_request_failed_session_retrieval,
)
def test_should_raise_doc_scan_exception_for_session_retrieval(_, doc_scan_client):
    """
    :type doc_scan_client: DocScanClient
    """
    with pytest.raises(DocScanException) as ex:
        doc_scan_client.get_session(SOME_SESSION_ID)

    doc_scan_exception = ex.value  # type: DocScanException
    assert "Failed to retrieve session" in str(doc_scan_exception)
    assert doc_scan_exception.status_code == 400


@mock.patch(
    "yoti_python_sdk.http.SignedRequest.execute",
    side_effect=mocked_request_server_error,
)
def test_should_raise_exception_for_delete_session(_, doc_scan_client):
    """
    :type doc_scan_client: DocScanClient
    """
    with pytest.raises(DocScanException) as ex:
        doc_scan_client.delete_session(SOME_SESSION_ID)

    doc_scan_exception = ex.value  # type: DocScanException
    assert "Failed to delete session" in str(doc_scan_exception)
    assert doc_scan_exception.status_code == 500


@mock.patch(
    "yoti_python_sdk.http.SignedRequest.execute",
    side_effect=mocked_request_not_found,
)
def test_should_raise_exception_for_invalid_content(_, doc_scan_client):
    """
    :type doc_scan_client: DocScanClient
    """
    with pytest.raises(DocScanException) as ex:
        doc_scan_client.get_media_content(SOME_SESSION_ID, SOME_MEDIA_ID)

    doc_scan_exception = ex.value  # type: DocScanException
    assert "Failed to retrieve media content" in str(doc_scan_exception)
    assert doc_scan_exception.status_code == 404


@mock.patch(
    "yoti_python_sdk.http.SignedRequest.execute",
    side_effect=mocked_request_media_content,
)
def test_should_return_media_value(_, doc_scan_client):
    """
    :type doc_scan_client: DocScanClient
    """
    media = doc_scan_client.get_media_content(SOME_SESSION_ID, SOME_MEDIA_ID)

    assert media.mime_type == "application/json"
    assert media.content == b"someContent"


@mock.patch(
    "yoti_python_sdk.http.SignedRequest.execute",
    side_effect=mocked_request_no_content,
)
def test_should_return_none_for_media_no_content(_, doc_scan_client):
    """
    :type doc_scan_client: DocScanClient
    """
    media = doc_scan_client.get_media_content(SOME_SESSION_ID, SOME_MEDIA_ID)

    assert media is None


@mock.patch(
    "yoti_python_sdk.http.SignedRequest.execute",
    side_effect=mocked_request_not_found,
)
def test_should_throw_exception_for_delete_media(_, doc_scan_client):
    """
    :type doc_scan_client: DocScanClient
    """
    with pytest.raises(DocScanException) as ex:
        doc_scan_client.delete_media_content(SOME_SESSION_ID, SOME_MEDIA_ID)

    doc_scan_exception = ex.value  # type: DocScanException
    assert "Failed to delete media content" in str(doc_scan_exception)
    assert 404 == doc_scan_exception.status_code


@mock.patch(
    "yoti_python_sdk.http.SignedRequest.execute",
    side_effect=mocked_supported_documents_content,
)
def test_should_return_supported_documents_response(_, doc_scan_client):
    """
    :type doc_scan_client: DocScanClient
    """
    supported_docs = doc_scan_client.get_supported_documents()

    assert len(supported_docs.supported_countries) == 2


@mock.patch(
    "yoti_python_sdk.http.SignedRequest.execute",
    side_effect=mocked_request_not_found,
)
def test_should_throw_exception_for_supported_documents(_, doc_scan_client):
    """
    :type doc_scan_client: DocScanClient
    """
    with pytest.raises(DocScanException) as ex:
        doc_scan_client.get_supported_documents()

    doc_scan_exception = ex.value
    assert "Failed to retrieve supported documents" in str(doc_scan_exception)
    assert 404 == doc_scan_exception.status_code


def test_should_use_correct_default_api_url(doc_scan_client):
    assert (
        doc_scan_client._DocScanClient__api_url
        == "https://api.yoti.com:443/idverify/v1"
    )  # noqa
