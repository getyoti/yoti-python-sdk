# -*- coding: utf-8 -*-
import pytz

from datetime import datetime

from yoti_python_sdk import config
from yoti_python_sdk.activity_details import ActivityDetails
from yoti_python_sdk.protobuf.protobuf import Protobuf


def create_selfie_field(activity_details):
    activity_details.field = lambda: None
    activity_details.field.name = config.ATTRIBUTE_SELFIE
    activity_details.field.value = "base64(ง •̀_•́)ง"
    activity_details.field.content_type = Protobuf.CT_STRING


def create_age_verified_field(
    activity_details, over, encoded_string_verified_value, age
):
    activity_details.field = lambda: None
    activity_details.field.name = (
        "age_over:{0}".format(age) if over is True else "age_under:".format(age)
    )
    activity_details.field.value = encoded_string_verified_value
    activity_details.field.content_type = Protobuf.CT_STRING


def create_structured_postal_address_field(activity_details, json_address_value):
    activity_details.field = lambda: None
    activity_details.field.name = config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS
    activity_details.field.value = json_address_value
    activity_details.field.content_type = Protobuf.CT_JSON


def test_failure_receipt_handled(failure_receipt, remember_me_id):
    activity_details = ActivityDetails(failure_receipt)

    assert activity_details.remember_me_id == remember_me_id
    assert activity_details.outcome == "FAILURE"
    assert activity_details.timestamp == datetime(
        2016, 11, 14, 11, 35, 33, tzinfo=pytz.utc
    )


def test_missing_values_handled(no_values_receipt):
    activity_details = ActivityDetails(no_values_receipt)

    assert isinstance(activity_details, ActivityDetails)


def test_remember_me_id_empty(empty_strings):
    activity_details = ActivityDetails(empty_strings)

    assert activity_details.remember_me_id == ""
    assert isinstance(activity_details, ActivityDetails)


def test_remember_me_id_valid(successful_receipt, remember_me_id):
    activity_details = ActivityDetails(successful_receipt)

    assert activity_details.remember_me_id == remember_me_id


def test_parent_remember_me_id_empty(empty_strings):
    activity_details = ActivityDetails(empty_strings)

    assert activity_details.remember_me_id == ""
    assert isinstance(activity_details, ActivityDetails)


def test_parent_remember_me_id_valid(successful_receipt, parent_remember_me_id):
    activity_details = ActivityDetails(successful_receipt)

    assert activity_details.parent_remember_me_id == parent_remember_me_id
