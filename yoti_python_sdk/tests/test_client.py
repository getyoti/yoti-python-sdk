# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from os import environ

import pytest
from cryptography.fernet import base64
from past.builtins import basestring

try:
    from unittest import mock
except ImportError:
    import mock

from yoti_python_sdk import YOTI_API_ENDPOINT
from yoti_python_sdk import Client
from yoti_python_sdk.config import SDK_IDENTIFIER
from yoti_python_sdk.client import NO_KEY_FILE_SPECIFIED_ERROR
from yoti_python_sdk.activity_details import ActivityDetails
from yoti_python_sdk.tests.conftest import YOTI_CLIENT_SDK_ID, PEM_FILE_PATH
from yoti_python_sdk.tests.mocks import (
    mocked_requests_get,
    mocked_requests_get_null_profile,
    mocked_requests_get_empty_profile,
    mocked_requests_get_missing_profile,
    mocked_timestamp,
    mocked_uuid4
)

INVALID_KEY_FILE_PATH = '/invalid/path/to/file.txt'
INVALID_KEY_FILES = (INVALID_KEY_FILE_PATH, 'wrong_pa&*#@th',
                     -19, 1, False, True, {}, [])


@pytest.fixture(scope='module')
def expected_headers(x_yoti_auth_key, x_yoti_auth_digest):
    return {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Yoti-Auth-Key': x_yoti_auth_key,
        'X-Yoti-Auth-Digest': x_yoti_auth_digest,
        'X-Yoti-SDK': SDK_IDENTIFIER
    }


@pytest.fixture(scope='module')
def expected_url(decrypted_request_token):
    nonce = mocked_uuid4()
    timestamp = int(mocked_timestamp() * 1000)
    return '{0}/profile/{1}?nonce={2}&timestamp={3}&appId={4}'.format(
        YOTI_API_ENDPOINT, decrypted_request_token,
        nonce, timestamp, YOTI_CLIENT_SDK_ID
    )


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
    expected_error = 'Could not read private key file'
    assert expected_error in str(exc)
    assert str(key_file) in str(exc)


@pytest.mark.parametrize('key_file', INVALID_KEY_FILES)
def test_creating_client_instance_with_invalid_key_file_env(key_file):
    environ['YOTI_KEY_FILE_PATH'] = str(key_file)
    with pytest.raises(RuntimeError) as exc:
        Client(YOTI_CLIENT_SDK_ID)
    expected_error = 'Could not read private key file'
    expected_error_source = 'specified by the YOTI_KEY_FILE_PATH env variable'
    assert expected_error in str(exc)
    assert expected_error_source in str(exc)
    assert str(key_file) in str(exc)


def test_creating_client_instance_with_invalid_key_file_env_but_valid_key_file_arg():
    environ['YOTI_KEY_FILE_PATH'] = INVALID_KEY_FILE_PATH
    Client(YOTI_CLIENT_SDK_ID, PEM_FILE_PATH)


def test_creating_client_instance_with_valid_key_file_env_but_invalid_key_file_arg():
    environ['YOTI_KEY_FILE_PATH'] = PEM_FILE_PATH
    with pytest.raises(RuntimeError) as exc:
        Client(YOTI_CLIENT_SDK_ID, INVALID_KEY_FILE_PATH)
    expected_error = 'Could not read private key file'
    assert expected_error in str(exc)
    assert str(INVALID_KEY_FILE_PATH) in str(exc)


@mock.patch('requests.get', side_effect=mocked_requests_get)
@mock.patch('time.time', side_effect=mocked_timestamp)
@mock.patch('uuid.uuid4', side_effect=mocked_uuid4)
def test_requesting_activity_details_with_correct_data(
        mock_uuid4, mock_time, mock_get, client, expected_url,
        expected_headers, encrypted_request_token):
    activity_details = client.get_activity_details(encrypted_request_token)

    mock_get.assert_called_once_with(url=expected_url, headers=expected_headers)
    assert isinstance(activity_details, ActivityDetails)
    assert activity_details.user_id == "ijH4kkqMKTG0FSNUgQIvd2Z3Nx1j8f5RjVQMyoKOvO/hkv43Ik+t6d6mGfP2tdrN"
    selfie = activity_details.user_profile.get('selfie')
    assert isinstance(selfie, basestring)
    base64_selfie_uri = getattr(activity_details, 'base64_selfie_uri')
    assert isinstance(base64_selfie_uri, basestring)
    assert base64_selfie_uri.startswith('data:image/jpeg;base64')


@mock.patch('requests.get', side_effect=mocked_requests_get_null_profile)
@mock.patch('time.time', side_effect=mocked_timestamp)
@mock.patch('uuid.uuid4', side_effect=mocked_uuid4)
def test_requesting_activity_details_with_null_profile(
        mock_uuid4, mock_time, mock_get, client, expected_url,
        expected_headers, encrypted_request_token):
    activity_details = client.get_activity_details(encrypted_request_token)

    mock_get.assert_called_once_with(url=expected_url, headers=expected_headers)
    assert activity_details.user_id == "ijH4kkqMKTG0FSNUgQIvd2Z3Nx1j8f5RjVQMyoKOvO/hkv43Ik+t6d6mGfP2tdrN"
    assert isinstance(activity_details, ActivityDetails)


@mock.patch('requests.get', side_effect=mocked_requests_get_empty_profile)
@mock.patch('time.time', side_effect=mocked_timestamp)
@mock.patch('uuid.uuid4', side_effect=mocked_uuid4)
def test_requesting_activity_details_with_empty_profile(
        mock_uuid4, mock_time, mock_get, client, expected_url,
        expected_headers, encrypted_request_token):
    activity_details = client.get_activity_details(encrypted_request_token)

    mock_get.assert_called_once_with(url=expected_url, headers=expected_headers)
    assert activity_details.user_id == "ijH4kkqMKTG0FSNUgQIvd2Z3Nx1j8f5RjVQMyoKOvO/hkv43Ik+t6d6mGfP2tdrN"
    assert isinstance(activity_details, ActivityDetails)


@mock.patch('requests.get', side_effect=mocked_requests_get_missing_profile)
@mock.patch('time.time', side_effect=mocked_timestamp)
@mock.patch('uuid.uuid4', side_effect=mocked_uuid4)
def test_requesting_activity_details_with_missing_profile(
        mock_uuid4, mock_time, mock_get, client, expected_url,
        expected_headers, encrypted_request_token):
    activity_details = client.get_activity_details(encrypted_request_token)

    mock_get.assert_called_once_with(url=expected_url, headers=expected_headers)
    assert activity_details.user_id == "ijH4kkqMKTG0FSNUgQIvd2Z3Nx1j8f5RjVQMyoKOvO/hkv43Ik+t6d6mGfP2tdrN"
    assert isinstance(activity_details, ActivityDetails)


@mock.patch('requests.get', side_effect=mocked_requests_get)
@mock.patch('time.time', side_effect=mocked_timestamp)
@mock.patch('uuid.uuid4', side_effect=mocked_uuid4)
def test_creating_request_with_unsupported_http_method(
        mock_uuid4, mock_time, mock_get, client, expected_headers):
    with pytest.raises(ValueError):
        client._Client__create_request(http_method="UNSUPPORTED_METHOD", path=YOTI_API_ENDPOINT, content=None)


@mock.patch('requests.get', side_effect=mocked_requests_get)
@mock.patch('uuid.uuid4', side_effect=mocked_uuid4)
@mock.patch('time.time', side_effect=mocked_timestamp)
def test_creating_request_with_supported_http_method(
        mock_uuid4, mock_time, mock_get, client, expected_headers):
    client._Client__create_request(http_method="GET", path=YOTI_API_ENDPOINT, content=None)


@mock.patch('requests.get', side_effect=mocked_requests_get)
@mock.patch('uuid.uuid4', side_effect=mocked_uuid4)
@mock.patch('time.time', side_effect=mocked_timestamp)
def test_creating_request_content_is_added(
        mock_uuid4, mock_time, mock_get, client, expected_headers):
    content = '{"Content"}'
    content_bytes = content.encode()
    request = client._Client__create_request(http_method="GET", path=YOTI_API_ENDPOINT, content=content_bytes)

    b64encoded = base64.b64encode(content_bytes)
    b64ascii = b64encoded.decode('ascii')

    assert request.endswith("&" + b64ascii)
