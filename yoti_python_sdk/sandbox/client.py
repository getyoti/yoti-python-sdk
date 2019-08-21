from yoti_python_sdk.sandbox.endpoint import SandboxEndpoint
from cryptography.fernet import base64
from os.path import expanduser, isfile
from past.builtins import basestring

import json
import requests
import yoti_python_sdk
from yoti_python_sdk.config import (
    X_YOTI_AUTH_KEY,
    X_YOTI_AUTH_DIGEST,
    X_YOTI_SDK,
    SDK_IDENTIFIER,
    X_YOTI_SDK_VERSION,
    JSON_CONTENT_TYPE,
)
from yoti_python_sdk.sandbox.token import YotiTokenRequest, YotiTokenResponse
from yoti_python_sdk.sandbox.attribute import SandboxAttribute
from yoti_python_sdk.sandbox.anchor import SandboxAnchor
from yoti_python_sdk.crypto import Crypto
from json import JSONEncoder


class SandboxEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, YotiTokenRequest):
            return o.__dict__()
        if isinstance(o, SandboxAttribute):
            return o.__dict__()
        if isinstance(o, SandboxAnchor):
            return o.__dict__()

        return json.JSONEncoder.default(self, o)


class SandboxClient(object):

    HTTP_SUPPORTED_METHODS = ["POST", "PUT", "PATCH", "GET", "DELETE"]

    def __init__(self, sdk_id, pem_file, sandbox_url):
        self.sdk_id = sdk_id
        self.__endpoint = SandboxEndpoint(sdk_id)
        self.__sandbox_url = sandbox_url

        pem_data = SandboxClient.__read_pem_file(
            pem_file, "failed in SandboxClient __init__"
        )

        self.__crypto = Crypto(pem_data)

    def setup_sharing_profile(self, request_token):
        request_path = self.__endpoint.get_sandbox_path()
        response = SandboxClient.post(
            self.__sandbox_url, request_path, self.__crypto, request_token
        )
        response_payload = response.json()
        return YotiTokenResponse(response_payload["token"])

    @staticmethod
    def builder():
        return SandboxClientBuilder()

    @staticmethod
    def post(host, path, key, content):
        payload = json.dumps(content, cls=SandboxEncoder)
        print(payload)
        payload_bytes = payload.encode()
        headers = SandboxClient.__get_request_headers(path, "POST", payload_bytes, key)
        return requests.post(host + path, payload_bytes, headers=headers, verify=False)

    @staticmethod
    def __get_request_headers(path, http_method, content, crypto):
        request = SandboxClient.__create_request(http_method, path, content)
        sdk_version = yoti_python_sdk.__version__

        return {
            X_YOTI_AUTH_KEY: crypto.get_public_key(),
            X_YOTI_AUTH_DIGEST: crypto.sign(request),
            X_YOTI_SDK: SDK_IDENTIFIER,
            X_YOTI_SDK_VERSION: "{0}-{1}".format(SDK_IDENTIFIER, sdk_version),
            "Content-Type": JSON_CONTENT_TYPE,
            "Accept": JSON_CONTENT_TYPE,
        }

    @staticmethod
    def __read_pem_file(key_file_path, error_source):
        try:
            key_file_path = expanduser(key_file_path)

            if not isinstance(key_file_path, basestring) or not isfile(key_file_path):
                raise IOError("File not found: {0}".format(key_file_path))
            with open(key_file_path, "rb") as pem_file:
                return pem_file.read().strip()
        except (AttributeError, IOError, TypeError, OSError) as exc:
            error = 'Could not read private key file: "{0}", passed as: {1} '.format(
                key_file_path, error_source
            )
            exception = "{0}: {1}".format(type(exc).__name__, exc)
            raise RuntimeError("{0}: {1}".format(error, exception))

    @staticmethod
    def __create_request(http_method, path, content):
        if http_method not in SandboxClient.HTTP_SUPPORTED_METHODS:
            raise ValueError(
                "{} is not in the list of supported methods: {}".format(
                    http_method, SandboxClient.HTTP_SUPPORTED_METHODS
                )
            )

        request = "{}&{}".format(http_method, path)

        if content is not None:
            b64encoded = base64.b64encode(content)
            b64ascii = b64encoded.decode("ascii")
            request += "&" + b64ascii

        return request


class SandboxClientBuilder(object):
    def __init__(self):
        self.__sdkId = None
        self.__pem_file = None

    def for_application(self, sdkId):
        self.__sdkId = sdkId
        return self

    def with_pem_file(self, pem_file):
        self.__pem_file = pem_file
        return self

    def build(self):
        if self.__sdkId is None or self.__pem_file is None:
            raise ValueError("SDK ID and/or pem file must not be None")

        return SandboxClient(self.__sdkId, self.__pem_file)
