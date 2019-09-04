# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from yoti_python_sdk import client

INVALID_DATA = "Json is incorrect, contains invalid data"
APPLICATION_NOT_FOUND = "Application was not found"
UNKNOWN_ERROR = "Unknown HTTP error occurred"


SHARE_URL_ERRORS = {
    400: "Json is incorrect, contains invalid data",
    404: "Application was not found",
}
SHARE_URL_ERRORS.update(client.DEFAULT_HTTP_CLIENT_ERRORS)


def create_share_url(yoti_client, dynamic_scenario):
    http_method = "POST"
    payload = json.dumps(dynamic_scenario, sort_keys=True).encode()
    endpoint = yoti_client.endpoints.get_dynamic_share_request_url(no_params=True)
    response = yoti_client.make_request(http_method, endpoint, payload)

    client.Client.http_error_handler(response, SHARE_URL_ERRORS)

    response_json = json.loads(response.text)

    return ShareUrl(
        _ShareUrl__qr_code=response_json["qrcode"],
        _ShareUrl__ref_id=response_json["ref_id"],
    )


class ShareUrl(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @property
    def share_url(self):
        return self.__qr_code

    @property
    def ref_id(self):
        return self.__ref_id
