from os.path import abspath
from os.path import dirname
from os.path import join

import pytest

from yoti_python_sdk.doc_scan.client import DocScanClient

FIXTURES_DIR = join(dirname(abspath(__file__)), "..", "fixtures")
PEM_FILE_PATH = join(FIXTURES_DIR, "sdk-test.pem")

YOTI_CLIENT_SDK_ID = "737204aa-d54e-49a4-8bde-26ddbe6d880c"


@pytest.fixture(scope="module")
def doc_scan_client():
    """
    :rtype: DocScanClient
    """
    return DocScanClient(YOTI_CLIENT_SDK_ID, PEM_FILE_PATH)
