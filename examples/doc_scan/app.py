import yoti_python_sdk
from flask import Flask, Response, render_template, request, session
from yoti_python_sdk.doc_scan import (
    DocScanClient,
    RequestedDocumentAuthenticityCheckBuilder,
    RequestedFaceMatchCheckBuilder,
    RequestedIDDocumentComparisonCheckBuilder,
    RequestedLivenessCheckBuilder,
    RequestedTextExtractionTaskBuilder,
    RequestedSupplementaryDocTextExtractionTaskBuilder,
    SdkConfigBuilder,
    SessionSpecBuilder,
    SessionOverviewPdfRequestBuilder,
)
from yoti_python_sdk.doc_scan.exception import DocScanException
from yoti_python_sdk.doc_scan.session.create.filter import (
    RequiredIdDocumentBuilder,
    DocumentRestrictionBuilder,
    DocumentRestrictionsFilterBuilder,
    RequiredSupplementaryDocumentBuilder,
)
from yoti_python_sdk.doc_scan.session.create.objective import (
    ProofOfAddressObjectiveBuilder,
)

from .settings import YOTI_APP_BASE_URL, YOTI_CLIENT_SDK_ID, YOTI_KEY_FILE_PATH

app = Flask(__name__)
app.secret_key = "someSecretKey"


def create_session():
    """
    Creates a Doc Scan session

    :return: the create session result
    :rtype: CreateSessionResult
    """
    doc_scan_client = DocScanClient(YOTI_CLIENT_SDK_ID, YOTI_KEY_FILE_PATH)

    sdk_config = (
        SdkConfigBuilder()
        .with_allows_camera_and_upload()
        .with_primary_colour("#2d9fff")
        .with_secondary_colour("#FFFFFF")
        .with_font_colour("#FFFFFF")
        .with_locale("en-GB")
        .with_preset_issuing_country("GBR")
        .with_success_url("{url}/success".format(url=YOTI_APP_BASE_URL))
        .with_error_url("{url}/error".format(url=YOTI_APP_BASE_URL))
        .with_privacy_policy_url("{url}/privacy-policy".format(url=YOTI_APP_BASE_URL))
        .build()
    )

    session_spec = (
        SessionSpecBuilder()
        .with_client_session_token_ttl(600)
        .with_resources_ttl(90000)
        .with_user_tracking_id("some-user-tracking-id")
        .with_requested_check(
            RequestedDocumentAuthenticityCheckBuilder()
            .with_manual_check_always()
            .build()
        )
        .with_requested_check(
            RequestedLivenessCheckBuilder()
            .for_zoom_liveness()
            .with_max_retries(1)
            .build()
        )
        .with_requested_check(
            RequestedFaceMatchCheckBuilder().with_manual_check_always().build()
        )
        .with_requested_check(RequestedIDDocumentComparisonCheckBuilder().build())
        .with_requested_task(
            RequestedTextExtractionTaskBuilder()
            .with_manual_check_always()
            .with_chip_data_desired()
            .build()
        )
        .with_requested_task(
            RequestedSupplementaryDocTextExtractionTaskBuilder()
            .with_manual_check_always()
            .build()
        )
        .with_sdk_config(sdk_config)
        .with_required_document(build_required_id_document_restriction("PASSPORT"))
        .with_required_document(RequiredIdDocumentBuilder().build())
        .with_required_document(
            RequiredSupplementaryDocumentBuilder()
            .with_objective(ProofOfAddressObjectiveBuilder().build())
            .build()
        )
        .build()
    )

    return doc_scan_client.create_session(session_spec)


def build_required_id_document_restriction(document_type):
    document_restriction = (
        DocumentRestrictionBuilder().with_document_types([document_type]).build()
    )

    filter_builder = DocumentRestrictionsFilterBuilder().for_whitelist()
    filter_builder.with_document_restriction(document_restriction)

    return RequiredIdDocumentBuilder().with_filter(filter_builder.build()).build()


@app.route("/")
def index():
    try:
        result = create_session()
    except DocScanException as e:
        return render_template("error.html", error=e.message)

    session["doc_scan_session_id"] = result.session_id

    iframe_url = "{base_url}/web/index.html?sessionID={session_id}&sessionToken={session_token}".format(
        base_url=yoti_python_sdk.YOTI_DOC_SCAN_API_URL,
        session_id=result.session_id,
        session_token=result.client_session_token,
    )

    return render_template("index.html", iframe_url=iframe_url)


@app.route("/success")
def success():
    doc_scan_client = DocScanClient(YOTI_CLIENT_SDK_ID, YOTI_KEY_FILE_PATH)

    session_id = session.get("doc_scan_session_id", None)

    try:
        session_result = doc_scan_client.get_session(session_id)
    except DocScanException as e:
        return render_template("error.html", error=e.message)

    return render_template("success.html", session_result=session_result)


@app.route("/error")
def error():
    error_message = "An unknown error occurred"

    if request.args.get("yotiErrorCode", None) is not None:
        error_message = "Error Code: {}".format(request.args.get("yotiErrorCode"))

    return render_template("error.html", error=error_message)


@app.route("/media")
def media():
    media_id = request.args.get("mediaId", None)
    if media_id is None:
        return Response(status=404)

    doc_scan_client = DocScanClient(YOTI_CLIENT_SDK_ID, YOTI_KEY_FILE_PATH)

    session_id = session.get("doc_scan_session_id", None)
    if session_id is None:
        return Response("No session ID available", status=404)

    try:
        retrieved_media = doc_scan_client.get_media_content(session_id, media_id)
    except DocScanException as e:
        return render_template("error.html", error=e.message)

    if retrieved_media is None:
        return Response("", status=204)

    return Response(
        retrieved_media.content, content_type=retrieved_media.mime_type, status=200
    )


@app.route("/session-pdf")
def session_pdf():
    """
    Generates and returns the session overview PDF for the current session.
    The PDF is streamed back to the browser as a downloadable file.
    """
    doc_scan_client = DocScanClient(YOTI_CLIENT_SDK_ID, YOTI_KEY_FILE_PATH)

    session_id = session.get("doc_scan_session_id", None)
    if session_id is None:
        return Response("No session ID available", status=404)

    include_images = request.args.get("include_images", None)
    include_extracted_text = request.args.get("include_extracted_text", None)
    include_device_tracking = request.args.get("include_device_tracking", None)

    pdf_request_builder = SessionOverviewPdfRequestBuilder()
    if include_images is not None:
        pdf_request_builder.with_include_images(include_images.lower() == "true")
    if include_extracted_text is not None:
        pdf_request_builder.with_include_extracted_text(
            include_extracted_text.lower() == "true"
        )
    if include_device_tracking is not None:
        pdf_request_builder.with_include_device_tracking(
            include_device_tracking.lower() == "true"
        )

    pdf_request = pdf_request_builder.build()

    try:
        pdf_bytes = doc_scan_client.create_session_overview_pdf(session_id, pdf_request)
    except DocScanException as e:
        return render_template("error.html", error=e.message)

    return Response(
        pdf_bytes,
        content_type="application/pdf",
        status=200,
        headers={
            "Content-Disposition": "attachment; filename=session-overview-{}.pdf".format(
                session_id
            )
        },
    )


@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy.html")


if __name__ == "__main__":
    app.run()
