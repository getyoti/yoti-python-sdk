# -*- coding: utf-8 -*-
from os import environ


DEFAULT_YOTI_API_URL = 'https://api.yoti.com'
DEFAULT_YOTI_API_VERSION = 'v1'
DEFAULT_YOTI_API_PORT = 443
DEFAULT_YOTI_CLIENT_SDK_ID = 'd13224e6-c8f4-4991-a703-b05fba4d4fdb'

YOTI_API_URL = environ.get('yoti_api_url', DEFAULT_YOTI_API_URL)
YOTI_API_VERSION = environ.get('yoti_api_version', DEFAULT_YOTI_API_VERSION)
YOTI_API_PORT = environ.get('yoti_api_port', DEFAULT_YOTI_API_PORT)
YOTI_API_ENDPOINT = '{0}/api/{1}'.format(YOTI_API_URL,
                                         YOTI_API_VERSION)
YOTI_CLIENT_SDK_ID = environ.get('yoti_client_sdk_id',
                                 DEFAULT_YOTI_CLIENT_SDK_ID)
