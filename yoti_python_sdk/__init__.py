# -*- coding: utf-8 -*-
import os
from distutils.util import convert_path
from os import environ

from yoti_python_sdk.client import Client

DEFAULTS = {
    "YOTI_API_URL": "https://api.yoti.com",
    "YOTI_API_PORT": 443,
    "YOTI_API_VERSION": "v1",
    "YOTI_API_VERIFY_SSL": "true",
}

main_ns = {}

directory_name = os.path.dirname(__file__)
version_path = os.path.join(directory_name, "version.py")

ver_path = convert_path(version_path)
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

__version__ = main_ns["__version__"]
YOTI_API_URL = environ.get("YOTI_API_URL", DEFAULTS["YOTI_API_URL"])

YOTI_PROFILE_ENDPOINT = "/api/v1"
YOTI_DOC_SCAN_ENDPOINT = "/idverify/v1"

YOTI_API_PORT = environ.get("YOTI_API_PORT", DEFAULTS["YOTI_API_PORT"])
YOTI_API_VERSION = environ.get("YOTI_API_VERSION", DEFAULTS["YOTI_API_VERSION"])

# Fully formatted API URLs
YOTI_API_ENDPOINT = environ.get(
    "YOTI_API_ENDPOINT",
    "{0}:{1}{2}".format(YOTI_API_URL, YOTI_API_PORT, YOTI_PROFILE_ENDPOINT),
)
YOTI_DOC_SCAN_API_URL = environ.get(
    "YOTI_DOC_SCAN_API_URL",
    "{0}:{1}{2}".format(YOTI_API_URL, YOTI_API_PORT, YOTI_DOC_SCAN_ENDPOINT),
)

YOTI_API_VERIFY_SSL = environ.get(
    "YOTI_API_VERIFY_SSL", DEFAULTS["YOTI_API_VERIFY_SSL"]
)
if YOTI_API_VERIFY_SSL.lower() == "false":
    YOTI_API_VERIFY_SSL = False
else:
    YOTI_API_VERIFY_SSL = True

__all__ = ["Client", __version__]
