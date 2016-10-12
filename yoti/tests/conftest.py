# -*- coding: utf-8 -*-
from os.path import dirname, join, abspath

import pytest

from yoti.crypto import Crypto

CURRENT_DIR = dirname(abspath(__file__))
PEM_FILE_PATH = join(CURRENT_DIR, 'fixtures/sdk-test.pem')
ENCRYPTED_TOKEN_FILE_PATH = join(CURRENT_DIR,
                                 'fixtures/encrypted_yoti_token.txt')


@pytest.fixture(scope='module')
def crypto():
    with open(PEM_FILE_PATH, 'rb') as pem_file:
        return Crypto(pem_file.read())


@pytest.fixture(scope='module')
def encrypted_request_token():
    with open(ENCRYPTED_TOKEN_FILE_PATH, 'rb') as token_file:
        return token_file.read()
