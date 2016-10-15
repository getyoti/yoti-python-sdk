# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from os import environ
from os.path import join, dirname

from yoti.client import Client, NO_KEY_FILE_SPECIFIED_ERROR


YOTI_CLIENT_SDK_ID = 'd13224e6-c8f4-4991-a703-b05fba4d4fdb'

CURRENT_DIR = dirname(__file__)
FIXTURES_PATH = join(CURRENT_DIR, 'fixtures')
PEM_FILE_PATH = join(FIXTURES_PATH, 'sdk-test.pem')

FORBIDDEN_KEY_FILE_PATH = 'yoti/tests/fixtures/forbidden-key.pem'
INVALID_KEY_FILE_PATH = '/invalid/path/to/file.txt'
INVALID_KEY_FILES = (INVALID_KEY_FILE_PATH, 'wrong_pa&*#@th',
                     -19, 1, False, True, {}, [])


@pytest.fixture(scope='module')
def client():
    return Client(YOTI_CLIENT_SDK_ID, PEM_FILE_PATH)


def test_creating_client_instance_with_valid_key_file_env():
    environ['YOTI_KEY_FILE_PATH'] = PEM_FILE_PATH
    Client(YOTI_CLIENT_SDK_ID)


def test_creating_client_instance_without_private_key_file():
    if environ.get('YOTI_KEY_FILE_PATH'):
        del environ['YOTI_KEY_FILE_PATH']
    with pytest.raises(RuntimeError) as exc:
        Client(YOTI_CLIENT_SDK_ID)
    assert str(exc.value) == NO_KEY_FILE_SPECIFIED_ERROR


@pytest.mark.parametrize('key_file', INVALID_KEY_FILES)
def test_creating_client_instance_with_invalid_key_file_arg(key_file):
    with pytest.raises(RuntimeError) as exc:
        Client(YOTI_CLIENT_SDK_ID, key_file)
    expected_error = 'Invalid private key file argument specified in Client()'
    assert expected_error in str(exc)
    assert str(key_file) in str(exc)


@pytest.mark.parametrize('key_file', INVALID_KEY_FILES)
def test_creating_client_instance_with_invalid_key_file_env(key_file):
    environ['YOTI_KEY_FILE_PATH'] = str(key_file)
    with pytest.raises(RuntimeError) as exc:
        Client(YOTI_CLIENT_SDK_ID)
    expected_error = 'Invalid private key file specified by the ' \
                     'YOTI_KEY_FILE_PATH env variable'
    assert expected_error in str(exc)
    assert str(key_file) in str(exc)


def test_creating_client_instance_with_invalid_key_file_env_but_valid_key_file_arg():
    environ['YOTI_KEY_FILE_PATH'] = INVALID_KEY_FILE_PATH
    Client(YOTI_CLIENT_SDK_ID, PEM_FILE_PATH)


def test_creating_client_instance_with_valid_key_file_env_but_invalid_key_file_arg():
    environ['YOTI_KEY_FILE_PATH'] = PEM_FILE_PATH
    with pytest.raises(RuntimeError) as exc:
        Client(YOTI_CLIENT_SDK_ID, INVALID_KEY_FILE_PATH)
    expected_error = 'Invalid private key file argument specified in Client()'
    assert expected_error in str(exc)
    assert str(INVALID_KEY_FILE_PATH) in str(exc)


# TODO: will be fixed in the next PR
# def test_requesting_activity_details_with_correct_token__should_yield_a_valid_encrypted_token(client, encrypted_request_token):
#     activity_details = client.get_activity_details(encrypted_request_token)
#     assert isinstance(activity_details, ActivityDetails)
#     assert activity_details.user_profile.get('selfie') is not None
