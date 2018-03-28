import pytest

from yoti_python_sdk.activity_details import ActivityDetails
from yoti_python_sdk.protobuf.v1.protobuf import Protobuf
from yoti_python_sdk.tests.conftest import successful_receipt


def create_selfie_field(activity_details):
    activity_details.field = lambda: None
    activity_details.field.name = "selfie"
    activity_details.field.value = "base64(ง •̀_•́)ง"
    activity_details.field.content_type = Protobuf.CT_STRING


def create_age_verified_field(activity_details, over, encoded_string_verified_value, age):
    activity_details.field = lambda: None
    activity_details.field.name = "age_over:{0}".format(age) if over is True else "age_under:".format(age)
    activity_details.field.value = encoded_string_verified_value
    activity_details.field.content_type = Protobuf.CT_STRING


def test_try_parse_selfie_field_valid_selfie():
    activity_details = ActivityDetails(successful_receipt())
    create_selfie_field(activity_details)

    ActivityDetails.try_parse_selfie_field(activity_details, activity_details.field)
    assert activity_details.base64_selfie_uri is not None


def test_try_parse_age_verified_both_missing_returns_null():
    activity_details = ActivityDetails(successful_receipt())
    create_selfie_field(activity_details)

    ActivityDetails.try_parse_age_verified_field(activity_details, activity_details.field)
    assert not activity_details.user_profile


def test_try_parse_age_verified_field_age_over():
    activity_details = ActivityDetails(successful_receipt())
    create_age_verified_field(activity_details, True, "true".encode(), 18)

    ActivityDetails.try_parse_age_verified_field(activity_details, activity_details.field)
    assert activity_details.user_profile['is_age_verified'] is True


def test_try_parse_age_verified_field_age_under():
    activity_details = ActivityDetails(successful_receipt())
    create_age_verified_field(activity_details, False, "false".encode(), 55)

    ActivityDetails.try_parse_age_verified_field(activity_details, activity_details.field)
    assert activity_details.user_profile['is_age_verified'] is False


def test_try_parse_age_verified_field_non_bool_value_throws_error():
    activity_details = ActivityDetails(successful_receipt())
    create_age_verified_field(activity_details, True, "18".encode(), 18)

    with pytest.raises(TypeError):
        ActivityDetails.try_parse_age_verified_field(activity_details, activity_details.field)
