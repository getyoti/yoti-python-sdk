from yoti_python_sdk.crypto import Crypto
from yoti_python_sdk.config import (
    X_YOTI_AUTH_KEY,
    X_YOTI_AUTH_DIGEST,
    X_YOTI_SDK,
    SDK_IDENTIFIER,
    X_YOTI_SDK_VERSION,
    JSON_CONTENT_TYPE,
)
from cryptography.fernet import base64
from urllib.parse import urlencode

import yoti_python_sdk
import requests
import uuid
import time

HTTP_POST = "POST"
HTTP_GET = "GET"
HTTP_SUPPORTED_METHODS = ["POST", "PUT", "PATCH", "GET", "DELETE"]


class SignedRequest(object):
    def __init__(self, base_url, crypto):
        self.__base_url = base_url
        self.__crypto = crypto

    def do_request(self, endpoint, http_method, payload=None, query_params=None):
        endpoint = endpoint + self.__append_query_params(query_params)
        headers = self.__get_request_headers(endpoint, http_method, payload)
        url = self.__base_url + endpoint

        return requests.request(
            method=http_method,
            url=url,
            data=payload,
            headers=headers,
            verify=yoti_python_sdk.YOTI_API_VERIFY_SSL,
        )

    def post(self, endpoint, payload=None, query_params=None):
        return self.do_request(
            endpoint, HTTP_POST, payload=payload, query_params=query_params
        )

    def get(self, endpoint, query_params=None):
        return self.do_request(endpoint, HTTP_GET, query_params=query_params)

    def __append_query_params(self, query_params=None):
        required = {
            "nonce": self.__create_nonce(),
            "timestamp": self.__create_timestamp(),
        }

        query_params = self.__merge_query_params(query_params, required)
        return "?{}".format(urlencode(query_params))

    @staticmethod
    def __merge_query_params(query_params, required):
        if query_params is None:
            return required

        merged = query_params.copy(query_params)
        merged.update(required)
        return merged

    def __get_request_headers(self, path, http_method, content):
        request = self.__create_request(http_method, path, content)
        sdk_version = yoti_python_sdk.__version__

        return {
            X_YOTI_AUTH_KEY: self.__crypto.get_public_key(),
            X_YOTI_AUTH_DIGEST: self.__crypto.sign(request),
            X_YOTI_SDK: SDK_IDENTIFIER,
            X_YOTI_SDK_VERSION: "{0}-{1}".format(SDK_IDENTIFIER, sdk_version),
            "Content-Type": JSON_CONTENT_TYPE,
            "Accept": JSON_CONTENT_TYPE,
        }

    @staticmethod
    def __create_request(http_method, path, content):
        if http_method not in HTTP_SUPPORTED_METHODS:
            raise ValueError(
                "{} is not in the list of supported methods: {}".format(
                    http_method, HTTP_SUPPORTED_METHODS
                )
            )

        request = "{}&{}".format(http_method, path)

        if content is not None:
            b64encoded = base64.b64encode(content)
            b64ascii = b64encoded.decode("ascii")
            request += "&" + b64ascii

        return request

    @staticmethod
    def __create_nonce():
        return uuid.uuid4()

    @staticmethod
    def __create_timestamp():
        return int(time.time() * 1000)

    @staticmethod
    def builder():
        return SignedRequestBuilder()


class SignedRequestBuilder(object):
    def __init__(self):
        self.__crypto = None
        self.__base_url = None

    def with_pem_file(self, pem_file):
        if isinstance(pem_file, Crypto):
            self.__crypto = pem_file
        else:
            self.__crypto = Crypto.read_pem_file(pem_file)

        return self

    def with_base_url(self, base_url):
        self.__base_url = base_url
        return self

    def build(self):
        if self.__crypto is None or self.__base_url is None:
            raise ValueError("Crypto and base URL must not be None")

        return SignedRequest(self.__base_url, self.__crypto)
