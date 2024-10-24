import json, requests
from flask import Flask, Response, request, render_template
    

from cryptography.fernet import base64

from settings import YOTI_API_URL, YOTI_CLIENT_SDK_ID, YOTI_KEY_FILE_PATH

from yoti_python_sdk.digital_identity import (
    DigitalIdentityClient
)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sessions")
def sessions():
    session_config = {
        "policy": {
            "wanted": [
                {
                    "name": "date_of_birth",
                    "derivation": "age_over:18",
                    "optional": "false"
                }
            ,
            {
                "name": "full_name"
            },
            {
                "name": "email_address"
            },
            {
                "name": "phone_number"
            },
            {
                "name": "selfie"
            },
            {
                "name": "date_of_birth",
                "derivation": "age_over:18"
            },
            {
                "name": "nationality"
            },
            {
                "name": "gender"
            },
            {
                "name": "document_details"
            },
            {
                "name": "document_images"
            }],
            "wanted_auth_types": [],
            "wanted_remember_me": "false",
        },
        "extensions": [],
        "subject": {
            "subject_id": "some_subject_id_string"
        }, # Optional reference to a user ID
        "notification": {
            "url": "https://webhook.site/818dc66b-e18b-4767-92c5-47c7af21629c",
            "method": "POST",
            "headers": {},
            "verifyTls": "true"
        },
        "redirectUri": "/profile" # Mandatory redirect URI but not required for Non-browser flows
    }

    digital_identity_client = DigitalIdentityClient(YOTI_CLIENT_SDK_ID, YOTI_KEY_FILE_PATH, YOTI_API_URL) 
    
    share_session_result = digital_identity_client.create_share_session(session_config)

    session_id = share_session_result.id

    # create_qr_code_result = create_share_qr_code(share_session_result.id)
    # get_share_session_result = get_share_session(share_session_result.id)
    # get_qr_code_result = get_share_qr_code(create_qr_code_result.id)
    
    # Return Session ID JSON
    return json.dumps({"session_id": session_id})

@app.route("/create-qr-code")
def create_qr_code():
    # Get query params - sessionId
    session_id = request.args.get('sessionId')
    digital_identity_client = DigitalIdentityClient(YOTI_CLIENT_SDK_ID, YOTI_KEY_FILE_PATH, YOTI_API_URL)

# Create QR Code
    create_qr_code_result = digital_identity_client.create_share_qr_code(session_id)

    # Return QR Code ID and URI JSON
    return json.dumps({"qr_code_id": create_qr_code_result.id, "qr_code_uri": create_qr_code_result.uri})

@app.route("/render-qr-code")
def render_qr_code():
    # Get query params - qrCodeUri
    qr_code_uri = request.args.get('qrCodeUri')
    # Make a POST request to the API to create a QR Code image
    url = "https://api.yoti.com/api/v1/qrcodes/image"
    payload = { "url": str(qr_code_uri) }
    headers = {
        "Accept": "image/png",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    # Return QR Code Image as PNG
    return Response(response.content, mimetype='image/png')

@app.route("/profile")
def profile():
    # Get query params - receiptId
    receipt_id = request.args.get('receiptId')
    digital_identity_client = DigitalIdentityClient(YOTI_CLIENT_SDK_ID, YOTI_KEY_FILE_PATH, YOTI_API_URL)

    share_receipt = digital_identity_client.get_share_receipt(receipt_id)
    age_over_verification = share_receipt.userContent.profile.find_age_over_verification(18)
    selfie = share_receipt.userContent.profile.selfie.value
    attribute_list = share_receipt.userContent.profile.attributes
    full_name = share_receipt.userContent.profile.full_name.value
    data = base64.b64encode(selfie).decode("utf-8")
    selfie_image = "data:{0};base64,{1}".format("image/jpeg", data)
    age_verified = age_over_verification.result

    return render_template("profile.html", age_verified=age_verified, selfie=selfie, full_name=full_name, selfie_image=selfie_image, attribute_list = attribute_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", ssl_context="adhoc")
