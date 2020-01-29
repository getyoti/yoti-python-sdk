from yoti_python_sdk.docs import DocScanClient
from yoti_python_sdk.docs import SessionSpecBuilder
from yoti_python_sdk.docs.session.create.check import DocumentAuthenticityCheckBuilder
from yoti_python_sdk.docs import NotificationConfigBuilder
from yoti_python_sdk.docs import SDKConfigBuilder
from os.path import join, dirname
from flask import Flask, render_template
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)
from settings import YOTI_CLIENT_SDK_ID, YOTI_KEY_FILE_PATH  # noqa

app = Flask(__name__)


@app.route("/")
def index():
    client = DocScanClient(YOTI_CLIENT_SDK_ID, YOTI_KEY_FILE_PATH)
    session = client.create_session(
        SessionSpecBuilder()
        .with_requested_checks(DocumentAuthenticityCheckBuilder().build())
        .with_notifications(
            NotificationConfigBuilder()
            .with_endpoint("https://example.com")
            .with_topics("session_completion")
            .build()
        )
        .with_sdk_config(
            SDKConfigBuilder()
            .with_success_url("https://localhost:5000/success")
            .with_error_url("https://localhost:5000")
            .build()
        )
        .build()
    )
    print("Doc Scan Session ID: %s" % session.client_session_id)

    return render_template(
        "index.html",
        session_id=session.client_session_id,
        client_token=session.client_session_token,
    )


@app.route("/success")
def success():
    return "Doc Scan request completed"


@app.route("/session/<session_id>")
def get_session(session_id):
    client = DocScanClient(YOTI_CLIENT_SDK_ID, YOTI_KEY_FILE_PATH)
    session = client.get_session(session_id)
    resources = [
        [page.media.id for page in document.pages]
        for document in session.resources.id_documents
    ]
    return "Session status: %s, Page Resources: %s" % (session.state, resources)


@app.route("/session/<session_id>/resource/<resource_id>")
def get_resource(session_id, resource_id):
    client = DocScanClient(YOTI_CLIENT_SDK_ID, YOTI_KEY_FILE_PATH)
    resource = client.get_media_content(session_id, resource_id)

    return '<img src="%s"/>' % resource.base64_content


if __name__ == "__main__":
    app.run(host="0.0.0.0", ssl_context="adhoc")
