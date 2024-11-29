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
            #.for_zoom_liveness()
            .for_static_liveness()
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


if __name__ == "__main__":
    app.run()
