# -*- coding: utf-8 -*-
import io
from os.path import abspath, dirname, join

import pytest

from yoti_python_sdk import Client
from yoti_python_sdk.crypto import Crypto
from yoti_python_sdk.tests.mocks import MockRequestHandler

FIXTURES_DIR = join(dirname(abspath(__file__)), "fixtures")
PEM_FILE_PATH = join(FIXTURES_DIR, "sdk-test.pem")
ENCRYPTED_TOKEN_FILE_PATH = join(FIXTURES_DIR, "encrypted_yoti_token.txt")
AUTH_KEY_FILE_PATH = join(FIXTURES_DIR, "auth_key.txt")
AUTH_DIGEST_GET_FILE_PATH = join(FIXTURES_DIR, "auth_digest_get.txt")
AUTH_DIGEST_POST_FILE_PATH = join(FIXTURES_DIR, "auth_digest_post.txt")

YOTI_CLIENT_SDK_ID = "737204aa-d54e-49a4-8bde-26ddbe6d880c"


@pytest.fixture(scope="module")
def mock_request_handler():
    return MockRequestHandler


@pytest.fixture(scope="module")
def client():
    return Client(YOTI_CLIENT_SDK_ID, PEM_FILE_PATH)


@pytest.fixture(scope="module")
def crypto():
    with open(PEM_FILE_PATH, "rb") as pem_file:
        return Crypto(pem_file.read())


@pytest.fixture(scope="module")
def encrypted_request_token():
    with open(ENCRYPTED_TOKEN_FILE_PATH, "rb") as token_file:
        return token_file.read()


@pytest.fixture(scope="module")
def decrypted_request_token():
    return (
        "i79CctmY-22ad195c-d166-49a2-af16-8f356788c9dd-be094d26-"
        "19b5-450d-afce-070101760f0b"
    )


@pytest.fixture(scope="module")
def user_id():
    return "ijH4kkqMKTG0FSNUgQIvd2Z3Nx1j8f5RjVQMyoKOvO/hkv43Ik+t6d6mGfP2tdrN"


@pytest.fixture(scope="module")
def parent_remember_me_id():
    return "f5RjVQMyoKOvO/hkv43Ik+t6d6mGfP2tdrNijH4k4qafTG0FSNUgQIvd2Z3Nx1j8"


@pytest.fixture(scope="module")
def receipt_id():
    return "Eq3+P8qjAlxr4d2mXKCUvzKdJTchI53ghwYPZXyA/cF5T+m/HCP1bK5LOmudZASN"


@pytest.fixture(scope="module")
def timestamp():
    return "2016-11-14T11:35:33Z"


@pytest.fixture(scope="module")
def successful_receipt(user_id, parent_remember_me_id, receipt_id, timestamp):
    return {
        "remember_me_id": user_id,
        "parent_remember_me_id": parent_remember_me_id,
        "receipt_id": receipt_id,
        "timestamp": timestamp,
        "sharing_outcome": "SUCCESS",
    }


@pytest.fixture(scope="module")
def failure_receipt(user_id, timestamp):
    return {
        "remember_me_id": user_id,
        "sharing_outcome": "FAILURE",
        "timestamp": timestamp,
    }


@pytest.fixture(scope="module")
def empty_strings():
    return {"remember_me_id": "", "parent_remember_me_id": "", "sharing_outcome": ""}


@pytest.fixture(scope="module")
def no_values_receipt():
    return {}


@pytest.fixture(scope="module")
def x_yoti_auth_key():
    with open(AUTH_KEY_FILE_PATH, "r") as auth_key_file:
        return auth_key_file.read()


@pytest.fixture(scope="module")
def x_yoti_auth_digest_get():
    with open(AUTH_DIGEST_GET_FILE_PATH, "r") as auth_digest_file:
        return auth_digest_file.read()


@pytest.fixture(scope="module")
def x_yoti_auth_digest_post():
    with io.open(
        AUTH_DIGEST_POST_FILE_PATH, mode="r", encoding="utf-8"
    ) as auth_digest_file:
        return auth_digest_file.read()
