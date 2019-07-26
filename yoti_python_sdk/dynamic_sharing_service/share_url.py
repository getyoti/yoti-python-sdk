# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

INVALID_DATA = "Json is incorrect, contains invalid data"
APPLICATION_NOT_FOUND = "Application was not found"
UNKNOWN_ERROR = "Unknown HTTP error occurred"


def create_share_url(yoti_client, dynamic_scenario):
    http_method = "POST"
    payload = json.dumps(dynamic_scenario, sort_keys=True).encode()
    endpoint = yoti_client.endpoints.get_dynamic_share_request_url()
    response = yoti_client.make_request(http_method, endpoint, payload)

    status_code = response.status_code
    if 200 <= status_code < 300:
        response_json = json.loads(response.text)

        return ShareUrl(
            _ShareUrl__qr_code=response_json["qrcode"],
            _ShareUrl__ref_id=response_json["ref_id"],
        )

    elif status_code == 400:
        raise RuntimeError(INVALID_DATA)
    elif status_code == 404:
        raise RuntimeError(APPLICATION_NOT_FOUND)
    else:
        raise RuntimeError(
            UNKNOWN_ERROR + ": " + str(status_code) + " " + response.text
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
