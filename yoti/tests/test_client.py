# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from os.path import join, dirname

import pytest

from yoti import YOTI_CLIENT_SDK_ID
from yoti.client import Client
from yoti.activity_details import ActivityDetails


CURRENT_DIR = dirname(__file__)
FIXTURES_PATH = join(CURRENT_DIR, 'fixtures')
PEM_FILE_PATH = join(FIXTURES_PATH, 'sdk-test.pem')


@pytest.fixture(scope='module')
def client():
    return Client(YOTI_CLIENT_SDK_ID, PEM_FILE_PATH)


def test_requesting_activity_details_with_correct_token__should_yield_a_valid_encrypted_token(client, encrypted_request_token):
    activity_details = client.get_activity_details(encrypted_request_token)
    assert isinstance(activity_details, ActivityDetails)
    assert activity_details.user_profile.get('selfie') is not None
