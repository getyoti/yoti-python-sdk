import json
import pytest

from yoti_python_sdk.doc_scan.client import DocScanClient  # noqa: F401
from yoti_python_sdk.doc_scan.exception import DocScanException
from yoti_python_sdk.doc_scan.session.create.session_spec import SessionSpec
from yoti_python_sdk.doc_scan.session.create.session_overview_pdf_request import (
    SessionOverviewPdfRequest,
    SessionOverviewPdfRequestBuilder,
)
from yoti_python_sdk.doc_scan.session.retrieve.create_session_result import (
    CreateSessionResult,
)
from yoti_python_sdk.doc_scan.session.retrieve.get_session_result import (
    GetSessionResult,
)
from yoti_python_sdk.tests.doc_scan.mocks import (
    mocked_request_failed_session_creation,
    mocked_request_failed_session_retrieval,
    mocked_request_failed_pdf_creation,
    mocked_request_media_content,
    mocked_request_no_content,
    mocked_request_not_found,
    mocked_request_server_error,
    mocked_request_successful_session_creation,
    mocked_request_successful_session_retrieval,
    mocked_request_successful_pdf_creation,
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


@mock.patch(
    "yoti_python_sdk.http.SignedRequest.execute",
    side_effect=mocked_request_successful_pdf_creation,
)
def test_should_return_pdf_bytes_on_successful_pdf_creation(_, doc_scan_client):
    """
    A 201 response from the PDF endpoint returns raw binary bytes unchanged.

    :type doc_scan_client: DocScanClient
    """
    pdf_request = SessionOverviewPdfRequestBuilder().with_include_images(True).build()

    result = doc_scan_client.create_session_overview_pdf(SOME_SESSION_ID, pdf_request)

    assert isinstance(result, bytes)
    assert result == b"%PDF-1.4 some pdf content"


@mock.patch(
    "yoti_python_sdk.http.SignedRequest.execute",
    side_effect=mocked_request_successful_pdf_creation,
)
def test_should_return_pdf_bytes_when_no_request_body_provided(_, doc_scan_client):
    """
    The request body model is optional; omitting it should not raise an error.

    :type doc_scan_client: DocScanClient
    """
    result = doc_scan_client.create_session_overview_pdf(SOME_SESSION_ID)

    assert isinstance(result, bytes)
    assert result == b"%PDF-1.4 some pdf content"


@mock.patch(
    "yoti_python_sdk.http.SignedRequest.execute",
    side_effect=mocked_request_failed_pdf_creation,
)
def test_should_raise_doc_scan_exception_for_failed_pdf_creation(_, doc_scan_client):
    """
    A non-201 response raises DocScanException with the expected message.

    :type doc_scan_client: DocScanClient
    """
    pdf_request = SessionOverviewPdfRequestBuilder().build()

    with pytest.raises(DocScanException) as ex:
        doc_scan_client.create_session_overview_pdf(SOME_SESSION_ID, pdf_request)

    doc_scan_exception = ex.value  # type: DocScanException
    assert "Failed to create session overview PDF" in str(doc_scan_exception)
    assert doc_scan_exception.status_code == 400


def _capture_pdf_request_body(doc_scan_client, pdf_request=None):
    """
    Calls create_session_overview_pdf and returns the JSON body that was
    actually handed to the HTTP layer.
    """
    captured = {}

    def fake_execute(signed_request):
        captured["data"] = signed_request.data
        return mocked_request_successful_pdf_creation()

    with mock.patch(
        "yoti_python_sdk.http.SignedRequest.execute",
        autospec=True,
        side_effect=fake_execute,
    ):
        if pdf_request is None:
            doc_scan_client.create_session_overview_pdf(SOME_SESSION_ID)
        else:
            doc_scan_client.create_session_overview_pdf(SOME_SESSION_ID, pdf_request)

    return json.loads(captured["data"].decode("utf-8"))


def test_pdf_request_body_should_nest_flags_under_options(doc_scan_client):
    pdf_request = (
        SessionOverviewPdfRequestBuilder()
        .with_include_images(True)
        .with_include_extracted_text(False)
        .with_include_device_tracking(True)
        .build()
    )

    body = _capture_pdf_request_body(doc_scan_client, pdf_request)

    assert body == {
        "options": {
            "include_images": True,
            "include_extracted_text": False,
            "include_device_tracking": True,
        }
    }


def test_pdf_request_body_should_omit_unset_flags_inside_options(doc_scan_client):
    pdf_request = SessionOverviewPdfRequestBuilder().with_include_images(True).build()

    body = _capture_pdf_request_body(doc_scan_client, pdf_request)

    assert body == {"options": {"include_images": True}}


def test_pdf_request_body_should_be_empty_options_when_no_request_given(
    doc_scan_client,
):
    body = _capture_pdf_request_body(doc_scan_client)

    assert body == {"options": {}}
