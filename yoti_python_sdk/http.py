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

import yoti_python_sdk
import requests
import uuid
import time

try:
    from urllib.parse import urlencode
except ImportError:
    from urlparse import urlencode

HTTP_POST = "POST"
HTTP_GET = "GET"
HTTP_SUPPORTED_METHODS = ["POST", "PUT", "PATCH", "GET", "DELETE"]


class SignedRequest(object):
    def __init__(self, url, http_method, payload, headers):
        self.__url = url
        self.__http_method = http_method
        self.__payload = payload
        self.__headers = headers

    @property
    def url(self):
        """
        Returns the URL for the SignedRequest
        """
        return self.__url

    @property
    def method(self):
        """
        Returns the HTTP method for the SignedRequest
        """
        return self.__http_method

    @property
    def data(self):
        """
        Returns the payload data for the SignedRequest
        """
        return self.__payload

    @property
    def headers(self):
        """
        Returns the HTTP headers for the SignedRequest
        """
        return self.__headers

    def prepare(self):
        """
        Creates a PreparedRequest object for use in a requests Session
        """
        r = requests.Request(
            method=self.method, url=self.url, headers=self.headers, data=self.data
        )
        return r.prepare()

    def execute(self):
        """
        Creates and sends a PreparedRequest in a requests Session, returning the requests Response object
        """
        prepared = self.prepare()
        with requests.Session() as s:
            return s.send(prepared)

    @staticmethod
    def builder():
        """
        Returns an instance of SignedRequestBuilder
        """
        return SignedRequestBuilder()


class SignedRequestBuilder(object):
    def __init__(self):
        self.__crypto = None
        self.__base_url = None
        self.__endpoint = None
        self.__http_method = None
        self.__params = None
        self.__headers = None
        self.__payload = None

    def with_pem_file(self, pem_file):
        """
        Sets the PEM file to be used for signing the request.  Can be an instance of yoti_python_sdk.crypto.Crypto
        or a path to a PEM file
        """
        if isinstance(pem_file, Crypto):
            self.__crypto = pem_file
        else:
            self.__crypto = Crypto.read_pem_file(pem_file)

        return self

    def with_base_url(self, base_url):
        """
        Sets the base URL for the signed request
        """
        self.__base_url = base_url
        return self

    def with_endpoint(self, endpoint):
        """
        Sets the endpoint for the signed request
        """
        self.__endpoint = endpoint
        return self

    def with_param(self, name, value):
        """
        Sets a query param to be used with the endpoint
        """
        if self.__params is None:
            self.__params = {}

        self.__params[name] = value
        return self

    def with_header(self, name, value):
        """
        Sets a HTTP header to be used in the request
        """
        if self.__headers is None:
            self.__headers = {}

        self.__headers[name] = value
        return self

    def with_http_method(self, http_method):
        """
        Sets the HTTP method to be used in the request
        """
        self.__http_method = http_method
        return self

    def with_post(self):
        """
        Sets the HTTP method for a POST request
        """
        self.with_http_method(HTTP_POST)
        return self

    def with_get(self):
        """
        Sets the HTTP method for a GET request
        """
        self.__http_method = HTTP_GET
        return self

    def __append_query_params(self, query_params=None):
        """
        Appends supplied query params in a dict to default query params.
        Returns a url encoded query param string
        """
        required = {
            "nonce": self.__create_nonce(),
            "timestamp": self.__create_timestamp(),
        }

        query_params = self.__merge_dictionary(query_params, required)
        return "?{}".format(urlencode(query_params))

    @staticmethod
    def __merge_dictionary(a, b):
        """
        Merges two dictionaries a and b, with b taking precedence over a
        """
        if a is None:
            return b

        merged = a.copy()
        merged.update(b)
        return merged

    def __get_request_headers(self, path, http_method, content):
        """
        Returns a dictionary of request headers, also using supplied headers from builder.  Default headers take precedence.
        """
        request = self.__create_request(http_method, path, content)
        sdk_version = yoti_python_sdk.__version__

        default = {
            X_YOTI_AUTH_KEY: self.__crypto.get_public_key(),
            X_YOTI_AUTH_DIGEST: self.__crypto.sign(request),
            X_YOTI_SDK: SDK_IDENTIFIER,
            X_YOTI_SDK_VERSION: "{0}-{1}".format(SDK_IDENTIFIER, sdk_version),
            "Content-Type": JSON_CONTENT_TYPE,
            "Accept": JSON_CONTENT_TYPE,
        }

        if self.__headers is not None:
            return self.__merge_dictionary(self.__headers, default)

        return default

    @staticmethod
    def __create_request(http_method, path, content):
        """
        Creates a concatenated string that is used in the X-YOTI-AUTH-DIGEST header
        :param http_method:
        :param path:
        :param content:
        :return:
        """
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

    def __validate_request(self):
        """
        Validates the request object to ensure the required values
        have been supplied.
        """
        if self.__base_url is None:
            raise ValueError("Base URL must not be None")
        if self.__endpoint is None:
            raise ValueError("Endpoint must not be None")
        if self.__crypto is None:
            raise ValueError("PEM file must not be None")
        if self.__http_method is None:
            raise ValueError("HTTP method must be specified")

    @staticmethod
    def __create_nonce():
        return uuid.uuid4()

    @staticmethod
    def __create_timestamp():
        return int(time.time() * 1000)

    def build(self):
        """
        Builds a SignedRequest object with the supplied values
        """
        self.__validate_request()

        endpoint = self.__endpoint + self.__append_query_params(self.__params)
        headers = self.__get_request_headers(
            endpoint, self.__http_method, self.__payload
        )
        url = self.__base_url + endpoint

        return SignedRequest(url, self.__http_method, self.__payload, headers)
