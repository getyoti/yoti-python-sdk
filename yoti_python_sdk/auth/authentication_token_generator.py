# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64
import json
import time
from os import environ

import requests

from yoti_python_sdk.crypto import Crypto
from .create_authentication_token_response import CreateAuthenticationTokenResponse
from .exception import AuthException

DEFAULT_AUTH_API_URL = "https://auth.api.yoti.com/v1/oauth/token"
CLIENT_ASSERTION_TYPE = "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"
JWT_EXPIRY_SECONDS = 300


class AuthenticationTokenGenerator(object):
    """
    Generates a central auth token that can be supplied to an SDK client
    (e.g. DocScanClient, Client) instead of a PEM file, allowing the Relying
    Business to authenticate using the new central auth scheme.

    The SDK does not automatically refresh or cache the generated token; the
    caller is responsible for generating a new one before it expires
    (see CreateAuthenticationTokenResponse.expires_in).
    """

    def __init__(self, sdk_id, crypto, auth_api_url):
        self.__sdk_id = sdk_id
        self.__crypto = crypto
        self.__auth_api_url = auth_api_url

    @staticmethod
    def builder():
        """
        Returns an instance of AuthenticationTokenGeneratorBuilder
        """
        return AuthenticationTokenGeneratorBuilder()

    def generate(self, scopes):
        """
        Generates an authentication token for the supplied scopes

        :param scopes: the scopes to request for the token
        :type scopes: list[str]
        :return: the generated token response
        :rtype: CreateAuthenticationTokenResponse
        :raises ValueError: if scopes is empty
        :raises AuthException: if the token could not be generated
        """
        if not scopes:
            raise ValueError("scopes must not be empty")

        client_assertion = self.__create_signed_jwt()
        form_data = {
            "grant_type": "client_credentials",
            "client_assertion_type": CLIENT_ASSERTION_TYPE,
            "client_assertion": client_assertion,
            "scope": " ".join(scopes),
        }

        response = requests.post(self.__auth_api_url, data=form_data)

        if response.status_code != 200:
            raise AuthException("Failed to generate authentication token", response)

        return CreateAuthenticationTokenResponse(json.loads(response.text))

    def __create_signed_jwt(self):
        """
        Creates a PS384-signed JWT client assertion, identifying the SDK by
        sdk_id and valid for JWT_EXPIRY_SECONDS
        """
        issuer = "sdk:{0}".format(self.__sdk_id)
        now = int(time.time())

        header = {"alg": "PS384", "typ": "JWT"}
        payload = {
            "iss": issuer,
            "sub": issuer,
            "aud": self.__auth_api_url,
            "iat": now,
            "exp": now + JWT_EXPIRY_SECONDS,
        }

        signing_input = "{0}.{1}".format(
            self.__base64url_encode(self.__json_dumps(header)),
            self.__base64url_encode(self.__json_dumps(payload)),
        )
        signature = self.__crypto.sign_ps384(signing_input.encode("utf-8"))

        return "{0}.{1}".format(signing_input, self.__base64url_encode(signature))

    @staticmethod
    def __json_dumps(data):
        return json.dumps(data, separators=(",", ":"), sort_keys=True).encode("utf-8")

    @staticmethod
    def __base64url_encode(data):
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


class AuthenticationTokenGeneratorBuilder(object):
    """
    Builder to assist in the creation of :class:`AuthenticationTokenGenerator`
    """

    def __init__(self):
        self.__sdk_id = None
        self.__crypto = None
        self.__auth_api_url = None

    def with_sdk_id(self, sdk_id):
        """
        Sets the SDK ID to identify the token request

        :param sdk_id: the SDK ID
        :type sdk_id: str
        :return: the builder
        :rtype: AuthenticationTokenGeneratorBuilder
        """
        self.__sdk_id = sdk_id
        return self

    def with_pem_file(self, pem_file):
        """
        Sets the PEM file used to sign the JWT client assertion.  Can be an
        instance of yoti_python_sdk.crypto.Crypto or a path to a PEM file

        :param pem_file: the PEM file or Crypto instance
        :return: the builder
        :rtype: AuthenticationTokenGeneratorBuilder
        """
        if isinstance(pem_file, Crypto):
            self.__crypto = pem_file
        else:
            self.__crypto = Crypto.read_pem_file(pem_file)

        return self

    def with_auth_api_url(self, auth_api_url):
        """
        Overrides the default auth API URL

        :param auth_api_url: the auth API URL
        :type auth_api_url: str
        :return: the builder
        :rtype: AuthenticationTokenGeneratorBuilder
        """
        self.__auth_api_url = auth_api_url
        return self

    def build(self):
        """
        Builds an AuthenticationTokenGenerator with the supplied values

        :return: the authentication token generator
        :rtype: AuthenticationTokenGenerator
        """
        if self.__sdk_id is None:
            raise ValueError("sdk_id must be provided")
        if self.__crypto is None:
            raise ValueError("pem_file must be provided")

        auth_api_url = self.__auth_api_url or environ.get(
            "YOTI_AUTH_URL", DEFAULT_AUTH_API_URL
        )

        return AuthenticationTokenGenerator(self.__sdk_id, self.__crypto, auth_api_url)
