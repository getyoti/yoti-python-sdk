# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from yoti_python_sdk.tests.conftest import PEM_FILE_PATH, YOTI_CLIENT_SDK_ID
from yoti_python_sdk.tests.mocks import (
    mocked_requests_post_share_url,
    mocked_requests_post_share_url_app_not_found,
    mocked_requests_post_share_url_invalid_json,
    mocked_timestamp,
    mocked_uuid4,
)

from yoti_python_sdk.dynamic_sharing_service import share_url
from yoti_python_sdk.dynamic_sharing_service.dynamic_scenario_builder import (
    DynamicScenarioBuilder,
)
from yoti_python_sdk.client import Client

try:
    from unittest import mock
except ImportError:
    import mock


@mock.patch("requests.request", side_effect=mocked_requests_post_share_url)
@mock.patch("time.time", side_effect=mocked_timestamp)
@mock.patch("uuid.uuid4", side_effect=mocked_uuid4)
def test_create_share_url_with_correct_data(mock_uuid4, mock_time, mock_get):
    yoti_client = Client(YOTI_CLIENT_SDK_ID, PEM_FILE_PATH)
    dynamic_scenario = DynamicScenarioBuilder().build()

    dynamic_share = share_url.create_share_url(yoti_client, dynamic_scenario)

    assert (
        dynamic_share.share_url == "https://code.yoti.com/forfhq3peurij4ihroiehg4jgiej"
    )
    assert dynamic_share.ref_id == "01aa2dea-d28b-11e6-bf26-cec0c932ce01"


@mock.patch("requests.request", side_effect=mocked_requests_post_share_url_invalid_json)
@mock.patch("time.time", side_effect=mocked_timestamp)
@mock.patch("uuid.uuid4", side_effect=mocked_uuid4)
def test_create_share_url_invalid_json(mock_uuid4, mock_time, mock_get):
    yoti_client = Client(YOTI_CLIENT_SDK_ID, PEM_FILE_PATH)
    dynamic_scenario = DynamicScenarioBuilder().build()

    with pytest.raises(RuntimeError) as err:
        share_url.create_share_url(yoti_client, dynamic_scenario)
    assert share_url.INVALID_DATA in str(err.value)


@mock.patch(
    "requests.request", side_effect=mocked_requests_post_share_url_app_not_found
)
@mock.patch("time.time", side_effect=mocked_timestamp)
@mock.patch("uuid.uuid4", side_effect=mocked_uuid4)
def test_create_share_url_app_not_found(mock_uuid4, mock_time, mock_get):
    yoti_client = Client(YOTI_CLIENT_SDK_ID, PEM_FILE_PATH)
    dynamic_scenario = DynamicScenarioBuilder().build()

    with pytest.raises(RuntimeError) as err:
        share_url.create_share_url(yoti_client, dynamic_scenario)
    assert share_url.APPLICATION_NOT_FOUND in str(err.value)
