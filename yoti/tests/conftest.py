# -*- coding: utf-8 -*-
from os.path import dirname, join, abspath

import pytest

from yoti.client import Client
from yoti.crypto import Crypto

FIXTURES_DIR = join(dirname(abspath(__file__)), 'fixtures')
PEM_FILE_PATH = join(FIXTURES_DIR, 'sdk-test.pem')
ENCRYPTED_TOKEN_FILE_PATH = join(FIXTURES_DIR, 'encrypted_yoti_token.txt')
AUTH_KEY_FILE_PATH = join(FIXTURES_DIR, 'auth_key.txt')
AUTH_DIGEST_FILE_PATH = join(FIXTURES_DIR, 'auth_digest.txt')

YOTI_CLIENT_SDK_ID = 'd13224e6-c8f4-4991-a703-b05fba4d4fdb'


@pytest.fixture(scope='module')
def client():
    return Client(YOTI_CLIENT_SDK_ID, PEM_FILE_PATH)


@pytest.fixture(scope='module')
def crypto():
    with open(PEM_FILE_PATH, 'rb') as pem_file:
        return Crypto(pem_file.read())


@pytest.fixture(scope='module')
def encrypted_request_token():
    with open(ENCRYPTED_TOKEN_FILE_PATH, 'rb') as token_file:
        return token_file.read()


@pytest.fixture(scope='module')
def decrypted_request_token():
    return 'NpdmVVGC-8b1e5780-6073-47d6-8d54-66ddcb34041b-ec7d01d4-fb9f-' \
           '4abb-97ad-5bd2ad5818f1'


@pytest.fixture(scope='module')
def x_yoti_auth_key():
    with open(AUTH_KEY_FILE_PATH, 'r') as auth_key_file:
        return auth_key_file.read()


@pytest.fixture(scope='module')
def x_yoti_auth_digest():
    with open(AUTH_DIGEST_FILE_PATH, 'r') as auth_digest_file:
        return auth_digest_file.read()
