from yoti_python_sdk.crypto import Crypto
from yoti_python_sdk.utils import create_nonce, create_timestamp
from yoti_python_sdk.config import (
    X_YOTI_AUTH_DIGEST,
    X_YOTI_SDK,
    SDK_IDENTIFIER,
    X_YOTI_SDK_VERSION,
    JSON_CONTENT_TYPE,
)
from cryptography.fernet import base64
from abc import ABCMeta, abstractmethod

import yoti_python_sdk
import requests

try:  # pragma: no cover
    from urllib.parse import urlencode
except ImportError:  # pragma: no cover
    from urllib import urlencode

HTTP_POST = "POST"
HTTP_GET = "GET"
HTTP_SUPPORTED_METHODS = ["POST", "PUT", "PATCH", "GET", "DELETE"]


class YotiResponse(object):
    def __init__(self, status_code, text, headers=None, content=None):
        if headers is None:
            headers = {}

        self.status_code = status_code
        self.text = text
        self.content = content
        self.headers = headers


class RequestHandler(object):
    """
    Default request handler for signing requests using the requests library.
    This type can be inherited and the execute method overridden to use any
    preferred HTTP library.  Must return type YotiResponse for use in the SDK.
    """

    __metaclass__ = ABCMeta  # Python 2 compatability

    @staticmethod
    @abstractmethod
    def execute(request):
        return NotImplemented


class DefaultRequestHandler(RequestHandler):
    @staticmethod
    def execute(request):
        """
        Execute the HTTP request supplied
        """
        if not isinstance(request, SignedRequest):
            raise TypeError("RequestHandler expects instance of SignedRequest")

        response = requests.request(
            url=request.url,
            method=request.method,
            data=request.data,
            headers=request.headers,
        )

        return YotiResponse(
            status_code=response.status_code,
            text=response.text,
            headers=response.headers,
            content=response.content,
        )


class SignedRequest(object):
    def __init__(self, url, http_method, payload, headers, request_handler=None):
        self.__url = url
        self.__http_method = http_method
        self.__payload = payload
        self.__headers = headers
        self.__request_handler = request_handler

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

    def execute(self):
        """
        Send the signed request, using the default RequestHandler if one has not be supplied
        """
        if self.__request_handler is None:
            return DefaultRequestHandler.execute(self)

        return self.__request_handler.execute(self)

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
        self.__request_handler = None

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

    def with_payload(self, payload):
        """
        Sets the payload for the signed request.  Must be a valid JSON string
        """
        self.__payload = payload
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
        if http_method not in HTTP_SUPPORTED_METHODS:
            raise ValueError("{} is an unsupported HTTP method".format(http_method))

        self.__http_method = http_method
        return self

    def with_request_handler(self, handler):
        # If no handler is passed, just return as the default will be used
        if handler is None:
            return self

        try:
            if not issubclass(handler, RequestHandler):
                raise TypeError(
                    "Handler must be instance of yoti_python_sdk.http.RequestHandler"
                )
        except Exception:
            # ABC
            raise TypeError(
                "Handler must be instance of yoti_python_sdk.http.RequestHandler"
            )

        self.__request_handler = handler
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
        self.with_http_method(HTTP_GET)
        return self

    def __append_query_params(self, query_params=None):
        """
        Appends supplied query params in a dict to default query params.
        Returns a url encoded query param string
        """
        required = {"nonce": create_nonce(), "timestamp": create_timestamp()}

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

        return SignedRequest(
            url, self.__http_method, self.__payload, headers, self.__request_handler
        )
