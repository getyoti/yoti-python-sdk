# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
import uuid
import json

import requests

from yoti import YOTI_API_ENDPOINT, YOTI_CLIENT_SDK_ID
from yoti.crypto import Crypto
from yoti.activity_details import ActivityDetails
from yoti.protobuf.v1 import protobuf


class Client(object):
    def __init__(self, sdk_id, pem_file_path):
        self.sdk_id = sdk_id

        with open(pem_file_path, 'rb') as pem_file:
            pem = pem_file.read()

        self.__crypto = Crypto(pem)

    def get_activity_details(self, encrypted_request_token):
        response = self.__make_request(encrypted_request_token)
        receipt = json.loads(response.text).get('receipt')

        encrypted_data = protobuf.Protobuf().current_user(receipt)

        unwrapped_key = self.__crypto.decrypt_token(
            receipt['wrapped_receipt_key']
        )
        decrypted_data = self.__crypto.decipher(
            unwrapped_key,
            encrypted_data.iv,
            encrypted_data.cipher_text
        )
        attribute_list = protobuf.Protobuf().attribute_list(decrypted_data)
        return ActivityDetails(receipt, attribute_list)

    def __make_request(self, encrypted_request_token):
        path = self.__get_request_path(encrypted_request_token)
        url = YOTI_API_ENDPOINT + path
        headers = self.__get_request_headers(path)
        response = requests.get(url=url, headers=headers)

        if not response.status_code == 200:
            raise RuntimeError(
                'Unsuccessful Yoti API call: {0}'.format(response.text))

        return response

    def __get_request_path(self, encrypted_request_token):
        token = self.__crypto.decrypt_token(encrypted_request_token).decode('utf-8')
        nonce = uuid.uuid4()
        timestamp_in_ms = int(time.time() * 1000)

        return '/profile/{0}?nonce={1}&timestamp_in_ms={2}&appId={3}'.format(
            token, nonce, timestamp_in_ms, YOTI_CLIENT_SDK_ID
        )

    def __get_request_headers(self, path):
        return {
            'X-Yoti-Auth-Key': self.__crypto.get_public_key(),
            'X-Yoti-Auth-Digest': self.__crypto.sign('GET&' + path),
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
