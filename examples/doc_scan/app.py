import base64
from io import BytesIO

import yoti_python_sdk
from filetype import filetype
from flask import Flask, Response, render_template, request, send_file, session
from yoti_python_sdk.doc_scan import (
    DocScanClient,
    RequestedDocumentAuthenticityCheckBuilder,
    RequestedFaceMatchCheckBuilder,
    RequestedLivenessCheckBuilder,
    RequestedTextExtractionTaskBuilder,
    SdkConfigBuilder,
    SessionSpecBuilder,
)
from yoti_python_sdk.doc_scan.exception import DocScanException

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
        .with_requested_check(RequestedDocumentAuthenticityCheckBuilder().build())
        .with_requested_check(
            RequestedLivenessCheckBuilder()
            .for_zoom_liveness()
            .with_max_retries(1)
            .build()
        )
        .with_requested_check(
            RequestedFaceMatchCheckBuilder().with_manual_check_fallback().build()
        )
        .with_requested_task(
            RequestedTextExtractionTaskBuilder().with_manual_check_always().build()
        )
        .with_sdk_config(sdk_config)
        .build()
    )

    return doc_scan_client.create_session(session_spec)


@app.route("/")
def index():
    try:
        result = create_session()
    except DocScanException as e:
        return render_template("error.html", error=e.text)

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
        return render_template("error.html", error=e.text)

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

    base64_req = request.args.get("base64", "0")

    session_id = session.get("doc_scan_session_id", None)
    if session_id is None:
        return Response("No session ID available", status=404)

    try:
        retrieved_media = doc_scan_client.get_media_content(session_id, media_id)
    except DocScanException as e:
        return render_template("error.html", error=e.text)

    if base64_req == "1" and retrieved_media.mime_type == "application/octet-stream":
        decoded = base64.b64decode(retrieved_media.content)
        info = filetype.guess(decoded)

        buffer = BytesIO()
        buffer.write(decoded)
        buffer.seek(0)

        return send_file(
            buffer,
            attachment_filename="media." + info.extension,
            mimetype=info.mime,
            as_attachment=True,
        )

    return Response(
        retrieved_media.content, content_type=retrieved_media.mime_type, status=200
    )


if __name__ == "__main__":
    app.run()
