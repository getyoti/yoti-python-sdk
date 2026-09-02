# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from abc import ABCMeta, abstractmethod

from cryptography.fernet import base64

from yoti_python_sdk.config import (
    AUTHORIZATION_HEADER,
    BEARER_PREFIX,
    X_YOTI_AUTH_DIGEST,
)
from yoti_python_sdk.utils import create_nonce, create_timestamp


class AuthStrategy(object):
    """
    Determines how outgoing SDK requests are authenticated against the Yoti API
    """

    __metaclass__ = ABCMeta  # Python 2 compatability

    @abstractmethod
    def create_auth_headers(self, http_method, endpoint, payload):
        """
        Returns a dict of HTTP headers required to authenticate the request
        """
        return NotImplemented

    @abstractmethod
    def create_query_params(self):
        """
        Returns a dict of query params required to authenticate the request
        """
        return NotImplemented


class SignedRequestStrategy(AuthStrategy):
    """
    Authenticates requests by signing them with an RSA private key,
    as used by the legacy signed-request scheme
    """

    def __init__(self, crypto):
        self.__crypto = crypto

    def create_auth_headers(self, http_method, endpoint, payload):
        signing_string = self.__create_signing_string(http_method, endpoint, payload)
        return {X_YOTI_AUTH_DIGEST: self.__crypto.sign(signing_string)}

    def create_query_params(self):
        return {"nonce": create_nonce(), "timestamp": create_timestamp()}

    @staticmethod
    def __create_signing_string(http_method, path, content):
        """
        Creates a concatenated string that is used in the X-Yoti-Auth-Digest header
        """
        signing_string = "{}&{}".format(http_method, path)

        if content is not None:
            b64encoded = base64.b64encode(content)
            signing_string += "&" + b64encoded.decode("ascii")

        return signing_string


class BearerTokenStrategy(AuthStrategy):
    """
    Authenticates requests using a central auth token, supplied as an
    Authorization header
    """

    def __init__(self, auth_token):
        if not auth_token:
            raise ValueError("auth_token must not be empty")

        self.__auth_token = auth_token

    def create_auth_headers(self, http_method, endpoint, payload):
        return {AUTHORIZATION_HEADER: BEARER_PREFIX + self.__auth_token}

    def create_query_params(self):
        return {}


class NoAuthStrategy(AuthStrategy):
    """
    Applies no authentication to the request
    """

    def create_auth_headers(self, http_method, endpoint, payload):
        return {}

    def create_query_params(self):
        return {}
