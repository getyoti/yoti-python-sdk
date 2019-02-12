# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from datetime import datetime
from os import environ

import pytest
from cryptography.fernet import base64
from past.builtins import basestring

from yoti_python_sdk import config

try:
    from unittest import mock
except ImportError:
    import mock

import yoti_python_sdk
from yoti_python_sdk import YOTI_API_ENDPOINT
from yoti_python_sdk import Client
from yoti_python_sdk import aml
from yoti_python_sdk.config import *
from yoti_python_sdk.client import NO_KEY_FILE_SPECIFIED_ERROR
from yoti_python_sdk.activity_details import ActivityDetails
from yoti_python_sdk.tests.conftest import YOTI_CLIENT_SDK_ID, PEM_FILE_PATH
from yoti_python_sdk.tests.mocks import (
    mocked_requests_get,
    mocked_requests_get_null_profile,
    mocked_requests_get_empty_profile,
    mocked_requests_get_missing_profile,
    mocked_requests_post_aml_profile,
    mocked_requests_post_aml_profile_not_found,
    mocked_timestamp,
    mocked_uuid4
)

INVALID_KEY_FILE_PATH = '/invalid/path/to/file.txt'
INVALID_KEY_FILES = (INVALID_KEY_FILE_PATH, 'wrong_pa&*#@th',
                     -19, 1, False, True, {}, [])


@pytest.fixture(scope='module')
def expected_get_headers(x_yoti_auth_key, x_yoti_auth_digest_get):
    sdk_version = yoti_python_sdk.__version__

    return {
        'Content-Type': JSON_CONTENT_TYPE,
        'Accept': JSON_CONTENT_TYPE,
        X_YOTI_AUTH_KEY: x_yoti_auth_key,
        X_YOTI_AUTH_DIGEST: x_yoti_auth_digest_get,
        X_YOTI_SDK: SDK_IDENTIFIER,
        X_YOTI_SDK_VERSION: sdk_version
    }


@pytest.fixture(scope='module')
def expected_post_headers(x_yoti_auth_key, x_yoti_auth_digest_post):
    sdk_version = yoti_python_sdk.__version__

    return {
        X_YOTI_AUTH_KEY: x_yoti_auth_key,
        X_YOTI_AUTH_DIGEST: x_yoti_auth_digest_post,
        X_YOTI_SDK: SDK_IDENTIFIER,
        X_YOTI_SDK_VERSION: sdk_version,
        'Content-Type': JSON_CONTENT_TYPE,
        'Accept': JSON_CONTENT_TYPE
    }


@pytest.fixture(scope='module')
def expected_activity_details_url(decrypted_request_token):
    nonce = mocked_uuid4()
    timestamp = int(mocked_timestamp() * 1000)
    return '{0}/profile/{1}?nonce={2}&timestamp={3}&appId={4}'.format(
        YOTI_API_ENDPOINT,
        decrypted_request_token,
        nonce,
        timestamp,
        YOTI_CLIENT_SDK_ID
    )


@pytest.fixture(scope='module')
def expected_aml_url():
    nonce = mocked_uuid4()
    timestamp = int(mocked_timestamp() * 1000)
    return '{0}/aml-check?appId={1}&timestamp={2}&nonce={3}'.format(
        YOTI_API_ENDPOINT,
        YOTI_CLIENT_SDK_ID,
        timestamp,
        nonce)


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
        mock_uuid4, mock_time, mock_get, client, expected_activity_details_url,
        expected_get_headers, encrypted_request_token):
    activity_details = client.get_activity_details(encrypted_request_token)

    mock_get.assert_called_once_with(url=expected_activity_details_url, headers=expected_get_headers)
    assert isinstance(activity_details, ActivityDetails)

    assert activity_details.user_id == "ijH4kkqMKTG0FSNUgQIvd2Z3Nx1j8f5RjVQMyoKOvO/hkv43Ik+t6d6mGfP2tdrN"
    assert activity_details.receipt_id == "Eq3+P8qjAlxr4d2mXKCUvzKdJTchI53ghwYPZXyA/cF5T+m/HCP1bK5LOmudZASN"
    assert activity_details.timestamp == datetime(2016, 11, 14, 11, 35, 33)

    selfie_user_profile = activity_details.user_profile.get(config.ATTRIBUTE_SELFIE)
    assert isinstance(selfie_user_profile, basestring)

    selfie_profile = activity_details.profile.selfie.value
    assert isinstance(selfie_profile, basestring)
    assert activity_details.profile.get_attribute(config.ATTRIBUTE_SELFIE) == activity_details.profile.selfie

    base64_selfie_uri = getattr(activity_details, config.KEY_BASE64_SELFIE)
    assert isinstance(base64_selfie_uri, basestring)
    assert base64_selfie_uri.startswith('data:image/jpeg;base64')


@mock.patch('requests.get', side_effect=mocked_requests_get_null_profile)
@mock.patch('time.time', side_effect=mocked_timestamp)
@mock.patch('uuid.uuid4', side_effect=mocked_uuid4)
def test_requesting_activity_details_with_null_profile(
        mock_uuid4, mock_time, mock_get, client, expected_activity_details_url,
        expected_get_headers, encrypted_request_token):
    activity_details = client.get_activity_details(encrypted_request_token)

    mock_get.assert_called_once_with(url=expected_activity_details_url, headers=expected_get_headers)
    assert activity_details.user_id == "ijH4kkqMKTG0FSNUgQIvd2Z3Nx1j8f5RjVQMyoKOvO/hkv43Ik+t6d6mGfP2tdrN"
    assert activity_details.receipt_id == "Eq3+P8qjAlxr4d2mXKCUvzKdJTchI53ghwYPZXyA/cF5T+m/HCP1bK5LOmudZASN"
    assert activity_details.timestamp == datetime(2016, 11, 14, 11, 35, 33)
    assert isinstance(activity_details, ActivityDetails)


@mock.patch('requests.get', side_effect=mocked_requests_get_empty_profile)
@mock.patch('time.time', side_effect=mocked_timestamp)
@mock.patch('uuid.uuid4', side_effect=mocked_uuid4)
def test_requesting_activity_details_with_empty_profile(
        mock_uuid4, mock_time, mock_get, client, expected_activity_details_url,
        expected_get_headers, encrypted_request_token):
    activity_details = client.get_activity_details(encrypted_request_token)

    mock_get.assert_called_once_with(url=expected_activity_details_url, headers=expected_get_headers)
    assert activity_details.user_id == "ijH4kkqMKTG0FSNUgQIvd2Z3Nx1j8f5RjVQMyoKOvO/hkv43Ik+t6d6mGfP2tdrN"
    assert activity_details.receipt_id == "Eq3+P8qjAlxr4d2mXKCUvzKdJTchI53ghwYPZXyA/cF5T+m/HCP1bK5LOmudZASN"
    assert activity_details.timestamp == datetime(2016, 11, 14, 11, 35, 33)
    assert isinstance(activity_details, ActivityDetails)


@mock.patch('requests.get', side_effect=mocked_requests_get_missing_profile)
@mock.patch('time.time', side_effect=mocked_timestamp)
@mock.patch('uuid.uuid4', side_effect=mocked_uuid4)
def test_requesting_activity_details_with_missing_profile(
        mock_uuid4, mock_time, mock_get, client, expected_activity_details_url,
        expected_get_headers, encrypted_request_token):
    activity_details = client.get_activity_details(encrypted_request_token)

    mock_get.assert_called_once_with(url=expected_activity_details_url, headers=expected_get_headers)
    assert activity_details.user_id == "ijH4kkqMKTG0FSNUgQIvd2Z3Nx1j8f5RjVQMyoKOvO/hkv43Ik+t6d6mGfP2tdrN"
    assert activity_details.receipt_id == "Eq3+P8qjAlxr4d2mXKCUvzKdJTchI53ghwYPZXyA/cF5T+m/HCP1bK5LOmudZASN"
    assert activity_details.timestamp == datetime(2016, 11, 14, 11, 35, 33)
    assert isinstance(activity_details, ActivityDetails)


@mock.patch('requests.get', side_effect=mocked_requests_get)
@mock.patch('time.time', side_effect=mocked_timestamp)
@mock.patch('uuid.uuid4', side_effect=mocked_uuid4)
def test_creating_request_with_unsupported_http_method(
        mock_uuid4, mock_time, mock_get, client, expected_get_headers):
    with pytest.raises(ValueError):
        client._Client__create_request(http_method="UNSUPPORTED_METHOD", path=YOTI_API_ENDPOINT, content=None)


@mock.patch('requests.get', side_effect=mocked_requests_get)
@mock.patch('uuid.uuid4', side_effect=mocked_uuid4)
@mock.patch('time.time', side_effect=mocked_timestamp)
def test_creating_request_with_supported_http_method(
        mock_uuid4, mock_time, mock_get, client, expected_get_headers):
    client._Client__create_request(http_method="GET", path=YOTI_API_ENDPOINT, content=None)


@mock.patch('requests.get', side_effect=mocked_requests_get)
@mock.patch('uuid.uuid4', side_effect=mocked_uuid4)
@mock.patch('time.time', side_effect=mocked_timestamp)
def test_creating_request_content_is_added(
        mock_uuid4, mock_time, mock_get, client, expected_get_headers):
    content = '{"Content"}'
    content_bytes = content.encode()
    request = client._Client__create_request(http_method="GET", path=YOTI_API_ENDPOINT, content=content_bytes)

    b64encoded = base64.b64encode(content_bytes)
    b64ascii = b64encoded.decode('ascii')

    assert request.endswith("&" + b64ascii)


@mock.patch('requests.post', side_effect=mocked_requests_post_aml_profile)
@mock.patch('time.time', side_effect=mocked_timestamp)
@mock.patch('uuid.uuid4', side_effect=mocked_uuid4)
def test_perform_aml_check_details_with_correct_data(
        mock_uuid4, mock_time, mock_post, client, expected_aml_url, expected_post_headers):
    given_names = "Given Name"
    family_name = "Family Name"

    aml_address = aml.AmlAddress(country="GBR")
    aml_profile = aml.AmlProfile(
        given_names,
        family_name,
        aml_address
    )

    aml_result = client.perform_aml_check(aml_profile)

    aml_profile_json = json.dumps(aml_profile.__dict__)
    aml_profile_bytes = aml_profile_json.encode()

    mock_post.assert_called_once_with(url=expected_aml_url, headers=expected_post_headers, data=aml_profile_bytes)

    assert isinstance(aml_result, aml.AmlResult)
    assert isinstance(aml_result.on_watch_list, bool)
    assert isinstance(aml_result.on_fraud_list, bool)
    assert isinstance(aml_result.on_pep_list, bool)


def test_perform_aml_check_with_null_profile(client):
    aml_profile = None

    with pytest.raises(TypeError) as exc:
        client.perform_aml_check(aml_profile)
    expected_error = 'aml_profile not set'
    assert expected_error in str(exc)


@mock.patch('requests.post', side_effect=mocked_requests_post_aml_profile_not_found)
@mock.patch('time.time', side_effect=mocked_timestamp)
@mock.patch('uuid.uuid4', side_effect=mocked_uuid4)
def test_perform_aml_check_with_unsuccessful_call(
        mock_uuid4, mock_time, mock_post, client):
    given_names = "Given Name"
    family_name = "Family Name"

    aml_address = aml.AmlAddress(country="GBR")
    aml_profile = aml.AmlProfile(
        given_names,
        family_name,
        aml_address
    )

    with pytest.raises(RuntimeError) as exc:
        client.perform_aml_check(aml_profile)
    expected_error = 'Unsuccessful Yoti API call:'
    assert expected_error in str(exc)
