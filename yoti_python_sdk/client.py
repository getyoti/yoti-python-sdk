# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from os import environ

import requests

import yoti_python_sdk
from yoti_python_sdk import aml
from yoti_python_sdk.activity_details import ActivityDetails
from yoti_python_sdk.crypto import Crypto
from yoti_python_sdk.endpoint import Endpoint
from yoti_python_sdk.http import SignedRequest
from yoti_python_sdk.protobuf import protobuf

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
        pem_file_path_env = environ.get("YOTI_KEY_FILE_PATH", pem_file_path)

        self.__crypto = Crypto.read_pem_file(pem_file_path_env)

        self.__signed_request = (
            SignedRequest.builder()
            .with_pem_file(self.__crypto)
            .with_base_url(yoti_python_sdk.YOTI_API_ENDPOINT)
            .build()
        )
        self.__endpoint = Endpoint(sdk_id)

    def get_activity_details(self, encrypted_request_token):
        content = None
        response = self.__make_activity_details_request(
            encrypted_request_token, content
        )
        receipt = json.loads(response.text).get("receipt")

        proto = protobuf.Protobuf()
        encrypted_data = proto.current_user(receipt)
        encrypted_application_profile = proto.current_application(receipt)

        if not encrypted_data:
            return ActivityDetails(receipt)

        unwrapped_key = self.__crypto.decrypt_token(receipt["wrapped_receipt_key"])

        decrypted_profile_data = self.__crypto.decipher(
            unwrapped_key, encrypted_data.iv, encrypted_data.cipher_text
        )
        decrypted_application_data = self.__crypto.decipher(
            unwrapped_key,
            encrypted_application_profile.iv,
            encrypted_application_profile.cipher_text,
        )

        user_profile_attribute_list = proto.attribute_list(decrypted_profile_data)
        application_profile_attribute_list = proto.attribute_list(
            decrypted_application_data
        )

        return ActivityDetails(
            receipt=receipt,
            decrypted_profile=user_profile_attribute_list,
            decrypted_application_profile=application_profile_attribute_list,
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
        response = requests.request(
            http_method,
            url,
            headers=headers,
            data=body,
            verify=yoti_python_sdk.YOTI_API_VERIFY_SSL,
        )
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

    def __make_activity_details_request(self, encrypted_request_token):
        decrypted_token = self.__crypto.decrypt_token(encrypted_request_token).decode(
            "utf-8"
        )
        query_params = {"appId": self.sdk_id}
        path = self.__endpoint.get_activity_details_request_path(
            decrypted_token, no_params=True
        )

        response = self.__signed_request.get(path, query_params)

        self.http_error_handler(
            response, {"default": "Unsuccessful Yoti API call: {} {}"}
        )

        return response

    def __make_aml_check_request(self, http_method, aml_profile):
        aml_profile_json = json.dumps(aml_profile.__dict__, sort_keys=True)
        aml_profile_bytes = aml_profile_json.encode()
        path = self.__endpoint.get_aml_request_url()
        url = yoti_python_sdk.YOTI_API_ENDPOINT + path
        headers = self.__get_request_headers(path, http_method, aml_profile_bytes)

        response = requests.post(
            url=url,
            headers=headers,
            data=aml_profile_bytes,
            verify=yoti_python_sdk.YOTI_API_VERIFY_SSL,
        )

        self.http_error_handler(
            response, {"default": "Unsuccessful Yoti API call: {} {}"}
        )

        return response
