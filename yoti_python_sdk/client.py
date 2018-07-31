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
from yoti_python_sdk.protobuf.v1 import protobuf
from .config import SDK_IDENTIFIER

NO_KEY_FILE_SPECIFIED_ERROR = 'Please specify the correct private key file ' \
                              'in Client(pem_file_path=...)\nor by setting ' \
                              'the "YOTI_KEY_FILE_PATH" environment variable'
HTTP_SUPPORTED_METHODS = ['POST', 'PUT', 'PATCH', 'GET', 'DELETE']


class Client(object):
    def __init__(self, sdk_id=None, pem_file_path=None):
        self.sdk_id = sdk_id or environ.get('YOTI_CLIENT_SDK_ID')
        pem_file_path_env = environ.get('YOTI_KEY_FILE_PATH')

        if pem_file_path is not None:
            error_source = 'argument specified in Client()'
            pem = self.__read_pem_file(pem_file_path, error_source)
        elif pem_file_path_env is not None:
            error_source = 'specified by the YOTI_KEY_FILE_PATH env variable'
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
                raise IOError('File not found: {0}'.format(key_file_path))
            with open(key_file_path, 'rb') as pem_file:
                return pem_file.read().strip()
        except (AttributeError, IOError, TypeError, OSError) as exc:
            error = 'Could not read private key file: "{0}", passed as: {1} '.format(key_file_path, error_source)
            exception = '{0}: {1}'.format(type(exc).__name__, exc)
            raise RuntimeError('{0}: {1}'.format(error, exception))

    def get_activity_details(self, encrypted_request_token):
        http_method = 'GET'
        content = None
        response = self.__make_activity_details_request(encrypted_request_token, http_method, content)
        receipt = json.loads(response.text).get('receipt')

        encrypted_data = protobuf.Protobuf().current_user(receipt)

        if not encrypted_data:
            return ActivityDetails(receipt)

        unwrapped_key = self.__crypto.decrypt_token(receipt['wrapped_receipt_key'])
        decrypted_data = self.__crypto.decipher(
            unwrapped_key,
            encrypted_data.iv,
            encrypted_data.cipher_text
        )
        attribute_list = protobuf.Protobuf().attribute_list(decrypted_data)
        return ActivityDetails(receipt, attribute_list)

    def perform_aml_check(self, aml_profile):
        if aml_profile is None:
            raise TypeError("aml_profile not set")

        http_method = 'POST'

        response = self.__make_aml_check_request(http_method, aml_profile)

        return aml.AmlResult(response.text)

    def __make_activity_details_request(self, encrypted_request_token, http_method, content):
        decrypted_token = self.__crypto.decrypt_token(encrypted_request_token).decode('utf-8')
        path = self.__endpoint.get_activity_details_request_path(decrypted_token)
        url = yoti_python_sdk.YOTI_API_ENDPOINT + path
        headers = self.__get_request_headers(path, http_method, content)
        response = requests.get(url=url, headers=headers)

        if not response.status_code == 200:
            raise RuntimeError('Unsuccessful Yoti API call: {0}'.format(response.text))

        return response

    def __make_aml_check_request(self, http_method, aml_profile):
        aml_profile_json = json.dumps(aml_profile.__dict__)
        aml_profile_bytes = aml_profile_json.encode()
        path = self.__endpoint.get_aml_request_url()
        url = yoti_python_sdk.YOTI_API_ENDPOINT + path
        headers = self.__get_request_headers(path, http_method, aml_profile_bytes)

        response = requests.post(url=url, headers=headers, data=aml_profile_bytes)

        if not response.status_code == 200:
            raise RuntimeError('Unsuccessful Yoti API call: {0}'.format(response.text))

        return response

    def __get_request_headers(self, path, http_method, content):
        request = self.__create_request(http_method, path, content)

        return {
            'X-Yoti-Auth-Key': self.__crypto.get_public_key(),
            'X-Yoti-Auth-Digest': self.__crypto.sign(request),
            'X-Yoti-SDK': SDK_IDENTIFIER,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    @staticmethod
    def __create_request(http_method, path, content):
        if http_method not in HTTP_SUPPORTED_METHODS:
            raise ValueError(
                "{} is not in the list of supported methods: {}".format(http_method, HTTP_SUPPORTED_METHODS))

        request = "{}&{}".format(http_method, path)

        if content is not None:
            b64encoded = base64.b64encode(content)
            b64ascii = b64encoded.decode('ascii')
            request += "&" + b64ascii

        return request
