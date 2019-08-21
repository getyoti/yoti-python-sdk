# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from os import environ
from os.path import isfile, expanduser

import requests
from cryptography.fernet import base64
from past.builtins import basestring

import yoti_python_sdk
from yoti_python_sdk import aml
from yoti_python_sdk.activity_details import ActivityDetails
from yoti_python_sdk.crypto import Crypto
from yoti_python_sdk.endpoint import Endpoint
from yoti_python_sdk.protobuf import protobuf
from .config import (
    X_YOTI_AUTH_KEY,
    X_YOTI_AUTH_DIGEST,
    X_YOTI_SDK,
    SDK_IDENTIFIER,
    X_YOTI_SDK_VERSION,
    JSON_CONTENT_TYPE,
)

NO_KEY_FILE_SPECIFIED_ERROR = (
    "Please specify the correct private key file "
    "in Client(pem_file_path=...)\nor by setting "
    'the "YOTI_KEY_FILE_PATH" environment variable'
)
HTTP_SUPPORTED_METHODS = ["POST", "PUT", "PATCH", "GET", "DELETE"]

UNKNOWN_HTTP_ERROR = "Unknown HTTP error occured: {0} {1}"
DEFAULT_HTTP_CLIENT_ERRORS = {"default": UNKNOWN_HTTP_ERROR}


class Client(object):
    def __init__(self, sdk_id=None, pem_file_path=None):
        self.sdk_id = sdk_id or environ.get("YOTI_CLIENT_SDK_ID")
        pem_file_path_env = environ.get("YOTI_KEY_FILE_PATH")

        if pem_file_path is not None:
            error_source = "argument specified in Client()"
            pem = self.__read_pem_file(pem_file_path, error_source)
        elif pem_file_path_env is not None:
            error_source = "specified by the YOTI_KEY_FILE_PATH env variable"
            pem = self.__read_pem_file(pem_file_path_env, error_source)
        else:
            raise RuntimeError(NO_KEY_FILE_SPECIFIED_ERROR)

        self.__crypto = Crypto(pem)
        self.__endpoint = Endpoint(sdk_id)

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

    def get_activity_details(self, encrypted_request_token):
        proto = protobuf.Protobuf()
        http_method = "GET"
        content = None
        response = self.__make_activity_details_request(
            encrypted_request_token, http_method, content
        )
        receipt = json.loads(response.text).get("receipt")

        encrypted_data = proto.current_user(receipt)
        encrypted_application_profile = proto.current_application(receipt)

        if not encrypted_data:
            return ActivityDetails(receipt)

        unwrapped_key = self.__crypto.decrypt_token(receipt["wrapped_receipt_key"])

        decrypted_profile_data = self.__crypto.decipher(
            unwrapped_key, encrypted_data.iv, encrypted_data.cipher_text
        )
        decrypted_application_data = self.__crypto.decipher(
            unwrapped_key, encrypted_application_profile.iv, encrypted_application_profile.cipher_text
        )

        user_profile_attribute_list = proto.attribute_list(decrypted_profile_data)
        application_profile_attribute_list = proto.attribute_list(decrypted_application_data)

        return ActivityDetails(
            receipt=receipt, decrypted_profile=user_profile_attribute_list, decrypted_application_profile=application_profile_attribute_list
        )

    def perform_aml_check(self, aml_profile):
        if aml_profile is None:
            raise TypeError("aml_profile not set")

        http_method = "POST"

        response = self.__make_aml_check_request(http_method, aml_profile)

        return aml.AmlResult(response.text)

    def make_request(self, http_method, endpoint, body):
        url = yoti_python_sdk.YOTI_API_ENDPOINT + endpoint
        headers = self.__get_request_headers(endpoint, http_method, body)
        response = requests.request(http_method, url, headers=headers, data=body, verify=yoti_python_sdk.YOTI_API_VERIFY_SSL)
        return response

    @property
    def endpoints(self):
        return self.__endpoint

    @staticmethod
    def http_error_handler(response, error_messages={}):
        status_code = response.status_code
        if 200 <= status_code < 300:
            return
        elif status_code in error_messages.keys():
            raise RuntimeError(
                error_messages[status_code].format(status_code, response.text)
            )
        elif "default" in error_messages.keys():
            raise RuntimeError(
                error_messages["default"].format(status_code, response.text)
            )
        else:
            raise RuntimeError(UNKNOWN_HTTP_ERROR.format(status_code, response.text))

    def __make_activity_details_request(
        self, encrypted_request_token, http_method, content
    ):
        decrypted_token = self.__crypto.decrypt_token(encrypted_request_token).decode(
            "utf-8"
        )
        path = self.__endpoint.get_activity_details_request_path(decrypted_token)
        url = yoti_python_sdk.YOTI_API_ENDPOINT + path
        headers = self.__get_request_headers(path, http_method, content)
        response = requests.get(url=url, headers=headers, verify=yoti_python_sdk.YOTI_API_VERIFY_SSL)

        self.http_error_handler(
            response, {"default": "Unsuccessful Yoti API call: {1}"}
        )

        return response

    def __make_aml_check_request(self, http_method, aml_profile):
        aml_profile_json = json.dumps(aml_profile.__dict__, sort_keys=True)
        aml_profile_bytes = aml_profile_json.encode()
        path = self.__endpoint.get_aml_request_url()
        url = yoti_python_sdk.YOTI_API_ENDPOINT + path
        headers = self.__get_request_headers(path, http_method, aml_profile_bytes)

        response = requests.post(url=url, headers=headers, data=aml_profile_bytes, verify=yoti_python_sdk.YOTI_API_VERIFY_SSL)

        self.http_error_handler(
            response, {"default": "Unsuccessful Yoti API call: {1}"}
        )

        return response

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
