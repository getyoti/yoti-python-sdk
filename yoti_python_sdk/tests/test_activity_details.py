# -*- coding: utf-8 -*-
import collections
import json
import os
import sys
from datetime import datetime

from yoti_python_sdk import config
from yoti_python_sdk.activity_details import ActivityDetails
from yoti_python_sdk.protobuf.protobuf import Protobuf
from yoti_python_sdk.tests.conftest import (
    successful_receipt,
    failure_receipt,
    no_values_receipt,
    user_id,
    parent_remember_me_id,
    empty_strings,
)

ADDRESS_FORMAT_KEY = "address_format"
ADDRESS_FORMAT_VALUE = 1
INDIA_FORMAT_VALUE = 2
USA_FORMAT_VALUE = 3

BUILDING_NUMBER_KEY = "building_number"
BUILDING_NUMBER_VALUE = "15a"

CARE_OF_KEY = "care_of"
CARE_OF_VALUE = "S/O: Name"

STATE_KEY = "state"
INDIA_STATE_VALUE = "Punjab"
USA_STATE_VALUE = "AL"

BUILDING_KEY = "building"
BUILDING_VALUE = "House No.1111-A"

STREET_KEY = "street"
STREET_VALUE = "42nd Street"

DISTRICT_KEY = "district"
DISTRICT_VALUE = "DISTRICT 10"

SUBDISTRICT_KEY = "subdistrict"
SUBDISTRICT_VALUE = "Sub-DISTRICT 10"

POST_OFFICE_KEY = "post_office"
INDIA_POST_OFFICE_VALUE = "Rajguru Nagar"

ADDRESS_LINE_1_KEY = "address_line_1"
ADDRESS_LINE_1_VALUE = "15a North Street"

TOWN_CITY_KEY = "town_city"
TOWN_CITY_VALUE = "TOWN/CITY NAME"

POSTAL_CODE_KEY = "postal_code"
POSTAL_CODE_VALUE = "SM5 2HW"
INDIA_POSTAL_CODE_VALUE = "141012"
USA_POSTAL_CODE_VALUE = "36201"

COUNTRY_ISO_KEY = "country_iso"
COUNTRY_ISO_VALUE = "GBR"
INDIA_COUNTRY_ISO_VALUE = "IND"
USA_COUNTRY_ISO_VALUE = "USA"

COUNTRY_KEY = "country"
COUNTRY_VALUE = "UK"
INDIA_COUNTRY_VALUE = "India"
USA_COUNTRY_VALUE = "USA"

FORMATTED_ADDRESS_VALUE = "15a North Street\nCARSHALTON\nSM5 2HW\nUK"
INDIA_FORMATTED_ADDRESS_VALUE = "S/O: Name\nHouse No.1111-A\n42nd Street\nTOWN/CITY NAME\nSub-DISTRICT 10\nDISTRICT 10\nPunjab\n141012\nRajgura Nagar\nIndia"
USA_FORMATTED_ADDRESS_VALUE = "15a North Street\nTOWN/CITY NAME\nAL\n36201\nUSA"


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
        "age_over:{0}".format(age) if over is True else "age_under:{0}".format(age)
    )
    activity_details.field.value = encoded_string_verified_value
    activity_details.field.content_type = Protobuf.CT_STRING


def create_structured_postal_address_field(activity_details, json_address_value):
    activity_details.field = lambda: None
    activity_details.field.name = config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS
    activity_details.field.value = json_address_value
    activity_details.field.content_type = Protobuf.CT_JSON


def test_try_parse_age_verified_both_missing_not_parsed(successful_receipt):
    activity_details = ActivityDetails(successful_receipt)
    field = None

    ActivityDetails.try_parse_age_verified_field(activity_details, field)
    assert not isinstance(
        activity_details.user_profile.get(config.KEY_AGE_VERIFIED), bool
    )


def test_failure_receipt_handled(failure_receipt, user_id):
    activity_details = ActivityDetails(failure_receipt)

    assert activity_details.user_id == user_id
    assert activity_details.remember_me_id == user_id
    assert activity_details.outcome == "FAILURE"
    assert activity_details.timestamp == datetime(2016, 11, 14, 11, 35, 33)


def test_missing_values_handled(no_values_receipt):
    activity_details = ActivityDetails(no_values_receipt)

    assert isinstance(activity_details, ActivityDetails)


def test_remember_me_id_empty(empty_strings):
    activity_details = ActivityDetails(empty_strings)

    assert activity_details.user_id == ""
    assert activity_details.remember_me_id == ""
    assert isinstance(activity_details, ActivityDetails)


def test_remember_me_id_valid(successful_receipt, user_id):
    activity_details = ActivityDetails(successful_receipt)

    assert activity_details.user_id == user_id
    assert activity_details.remember_me_id == user_id


def test_parent_remember_me_id_empty(empty_strings):
    activity_details = ActivityDetails(empty_strings)

    assert activity_details.user_id == ""
    assert activity_details.remember_me_id == ""
    assert isinstance(activity_details, ActivityDetails)


def test_parent_remember_me_id_valid(successful_receipt, parent_remember_me_id):
    activity_details = ActivityDetails(successful_receipt)

    assert activity_details.parent_remember_me_id == parent_remember_me_id


def test_try_parse_age_verified_field_age_over(successful_receipt):
    activity_details = ActivityDetails(successful_receipt)
    create_age_verified_field(activity_details, True, "true".encode(), 18)

    ActivityDetails.try_parse_age_verified_field(
        activity_details, activity_details.field
    )
    assert activity_details.user_profile[config.KEY_AGE_VERIFIED] is True


def test_try_parse_age_verified_field_age_under(successful_receipt):
    activity_details = ActivityDetails(successful_receipt)
    create_age_verified_field(activity_details, False, "false".encode(), 55)

    ActivityDetails.try_parse_age_verified_field(
        activity_details, activity_details.field
    )
    assert activity_details.user_profile[config.KEY_AGE_VERIFIED] is False


def test_try_parse_age_verified_field_non_bool_value_not_parsed(successful_receipt):
    activity_details = ActivityDetails(successful_receipt)
    create_age_verified_field(activity_details, True, "18".encode(), 18)
    sys.stdout = open(os.devnull, "w")  # disable print
    ActivityDetails.try_parse_age_verified_field(
        activity_details, activity_details.field
    )
    sys.stdout = sys.__stdout__  # enable print
    assert not isinstance(
        activity_details.user_profile.get(config.KEY_AGE_VERIFIED), bool
    )


def test_try_parse_structured_postal_address_uk(successful_receipt):
    activity_details = ActivityDetails(successful_receipt)
    structured_postal_address = {
        ADDRESS_FORMAT_KEY: ADDRESS_FORMAT_VALUE,
        BUILDING_NUMBER_KEY: BUILDING_NUMBER_VALUE,
        ADDRESS_LINE_1_KEY: ADDRESS_LINE_1_VALUE,
        TOWN_CITY_KEY: TOWN_CITY_VALUE,
        POSTAL_CODE_KEY: POSTAL_CODE_VALUE,
        COUNTRY_ISO_KEY: COUNTRY_ISO_VALUE,
        COUNTRY_KEY: COUNTRY_VALUE,
        config.KEY_FORMATTED_ADDRESS: FORMATTED_ADDRESS_VALUE,
    }

    structured_postal_address_json = json.dumps(structured_postal_address)

    create_structured_postal_address_field(
        activity_details, structured_postal_address_json
    )

    activity_details.user_profile[
        config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS
    ] = ActivityDetails.try_convert_structured_postal_address_to_dict(
        activity_details.field
    )

    actual_structured_postal_address_user_profile = activity_details.user_profile[
        config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS
    ]

    assert (
        type(actual_structured_postal_address_user_profile) is collections.OrderedDict
    )
    assert (
        actual_structured_postal_address_user_profile[ADDRESS_FORMAT_KEY]
        == ADDRESS_FORMAT_VALUE
    )
    assert (
        actual_structured_postal_address_user_profile[BUILDING_NUMBER_KEY]
        == BUILDING_NUMBER_VALUE
    )
    assert (
        actual_structured_postal_address_user_profile[ADDRESS_LINE_1_KEY]
        == ADDRESS_LINE_1_VALUE
    )
    assert (
        actual_structured_postal_address_user_profile[TOWN_CITY_KEY] == TOWN_CITY_VALUE
    )
    assert (
        actual_structured_postal_address_user_profile[POSTAL_CODE_KEY]
        == POSTAL_CODE_VALUE
    )
    assert (
        actual_structured_postal_address_user_profile[COUNTRY_ISO_KEY]
        == COUNTRY_ISO_VALUE
    )
    assert actual_structured_postal_address_user_profile[COUNTRY_KEY] == COUNTRY_VALUE
    assert (
        actual_structured_postal_address_user_profile[config.KEY_FORMATTED_ADDRESS]
        == FORMATTED_ADDRESS_VALUE
    )


def test_try_parse_structured_postal_address_india(successful_receipt):
    activity_details = ActivityDetails(successful_receipt)
    structured_postal_address = {
        ADDRESS_FORMAT_KEY: INDIA_FORMAT_VALUE,
        CARE_OF_KEY: CARE_OF_VALUE,
        BUILDING_KEY: BUILDING_VALUE,
        STREET_KEY: STREET_VALUE,
        TOWN_CITY_KEY: TOWN_CITY_VALUE,
        SUBDISTRICT_KEY: SUBDISTRICT_VALUE,
        DISTRICT_KEY: DISTRICT_VALUE,
        STATE_KEY: INDIA_STATE_VALUE,
        POSTAL_CODE_KEY: INDIA_POSTAL_CODE_VALUE,
        POST_OFFICE_KEY: INDIA_POST_OFFICE_VALUE,
        COUNTRY_ISO_KEY: INDIA_COUNTRY_ISO_VALUE,
        COUNTRY_KEY: INDIA_COUNTRY_VALUE,
        config.KEY_FORMATTED_ADDRESS: INDIA_FORMATTED_ADDRESS_VALUE,
    }

    structured_postal_address_json = json.dumps(structured_postal_address)

    create_structured_postal_address_field(
        activity_details, structured_postal_address_json
    )

    activity_details.user_profile[
        config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS
    ] = ActivityDetails.try_convert_structured_postal_address_to_dict(
        activity_details.field
    )

    actual_structured_postal_address_user_profile = activity_details.user_profile[
        config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS
    ]

    assert (
        type(actual_structured_postal_address_user_profile) is collections.OrderedDict
    )
    assert (
        actual_structured_postal_address_user_profile[ADDRESS_FORMAT_KEY]
        == INDIA_FORMAT_VALUE
    )
    assert actual_structured_postal_address_user_profile[CARE_OF_KEY] == CARE_OF_VALUE
    assert actual_structured_postal_address_user_profile[BUILDING_KEY] == BUILDING_VALUE
    assert actual_structured_postal_address_user_profile[STREET_KEY] == STREET_VALUE
    assert (
        actual_structured_postal_address_user_profile[TOWN_CITY_KEY] == TOWN_CITY_VALUE
    )
    assert (
        actual_structured_postal_address_user_profile[SUBDISTRICT_KEY]
        == SUBDISTRICT_VALUE
    )
    assert actual_structured_postal_address_user_profile[DISTRICT_KEY] == DISTRICT_VALUE
    assert actual_structured_postal_address_user_profile[STATE_KEY] == INDIA_STATE_VALUE
    assert (
        actual_structured_postal_address_user_profile[POSTAL_CODE_KEY]
        == INDIA_POSTAL_CODE_VALUE
    )
    assert (
        actual_structured_postal_address_user_profile[POST_OFFICE_KEY]
        == INDIA_POST_OFFICE_VALUE
    )
    assert (
        actual_structured_postal_address_user_profile[COUNTRY_ISO_KEY]
        == INDIA_COUNTRY_ISO_VALUE
    )
    assert (
        actual_structured_postal_address_user_profile[COUNTRY_KEY]
        == INDIA_COUNTRY_VALUE
    )
    assert (
        actual_structured_postal_address_user_profile[config.KEY_FORMATTED_ADDRESS]
        == INDIA_FORMATTED_ADDRESS_VALUE
    )


def test_try_parse_structured_postal_address_usa(successful_receipt):
    activity_details = ActivityDetails(successful_receipt)
    structured_postal_address = {
        ADDRESS_FORMAT_KEY: USA_FORMAT_VALUE,
        ADDRESS_LINE_1_KEY: ADDRESS_LINE_1_VALUE,
        TOWN_CITY_KEY: TOWN_CITY_VALUE,
        STATE_KEY: USA_STATE_VALUE,
        POSTAL_CODE_KEY: USA_POSTAL_CODE_VALUE,
        COUNTRY_ISO_KEY: USA_COUNTRY_ISO_VALUE,
        COUNTRY_KEY: USA_COUNTRY_VALUE,
        config.KEY_FORMATTED_ADDRESS: USA_FORMATTED_ADDRESS_VALUE,
    }

    structured_postal_address_json = json.dumps(structured_postal_address)

    create_structured_postal_address_field(
        activity_details, structured_postal_address_json
    )

    activity_details.user_profile[
        config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS
    ] = ActivityDetails.try_convert_structured_postal_address_to_dict(
        activity_details.field
    )

    actual_structured_postal_address_user_profile = activity_details.user_profile[
        config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS
    ]

    assert (
        type(actual_structured_postal_address_user_profile) is collections.OrderedDict
    )
    assert (
        actual_structured_postal_address_user_profile[ADDRESS_FORMAT_KEY]
        == USA_FORMAT_VALUE
    )
    assert (
        actual_structured_postal_address_user_profile[ADDRESS_LINE_1_KEY]
        == ADDRESS_LINE_1_VALUE
    )
    assert (
        actual_structured_postal_address_user_profile[TOWN_CITY_KEY] == TOWN_CITY_VALUE
    )
    assert actual_structured_postal_address_user_profile[STATE_KEY] == USA_STATE_VALUE
    assert (
        actual_structured_postal_address_user_profile[POSTAL_CODE_KEY]
        == USA_POSTAL_CODE_VALUE
    )
    assert (
        actual_structured_postal_address_user_profile[COUNTRY_ISO_KEY]
        == USA_COUNTRY_ISO_VALUE
    )
    assert (
        actual_structured_postal_address_user_profile[COUNTRY_KEY] == USA_COUNTRY_VALUE
    )
    assert (
        actual_structured_postal_address_user_profile[config.KEY_FORMATTED_ADDRESS]
        == USA_FORMATTED_ADDRESS_VALUE
    )


def test_try_parse_structured_postal_address_nested_json(successful_receipt):
    formatted_address_json = {
        "item1": [[1, "a1"], [2, "a2"]],
        "item2": [[3, "b3"], [4, "b4"]],
    }

    activity_details = ActivityDetails(successful_receipt)
    structured_postal_address = {
        ADDRESS_FORMAT_KEY: ADDRESS_FORMAT_VALUE,
        BUILDING_NUMBER_KEY: BUILDING_NUMBER_VALUE,
        ADDRESS_LINE_1_KEY: ADDRESS_LINE_1_VALUE,
        TOWN_CITY_KEY: TOWN_CITY_VALUE,
        POSTAL_CODE_KEY: POSTAL_CODE_VALUE,
        COUNTRY_ISO_KEY: COUNTRY_ISO_VALUE,
        COUNTRY_KEY: COUNTRY_VALUE,
        config.KEY_FORMATTED_ADDRESS: formatted_address_json,
    }

    structured_postal_address_json = json.dumps(structured_postal_address)

    create_structured_postal_address_field(
        activity_details, structured_postal_address_json
    )

    activity_details.user_profile[
        config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS
    ] = ActivityDetails.try_convert_structured_postal_address_to_dict(
        activity_details.field
    )

    actual_structured_postal_address_user_profile = activity_details.user_profile[
        config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS
    ]

    assert (
        type(actual_structured_postal_address_user_profile) is collections.OrderedDict
    )
    assert (
        actual_structured_postal_address_user_profile[ADDRESS_FORMAT_KEY]
        == ADDRESS_FORMAT_VALUE
    )
    assert (
        actual_structured_postal_address_user_profile[BUILDING_NUMBER_KEY]
        == BUILDING_NUMBER_VALUE
    )
    assert (
        actual_structured_postal_address_user_profile[ADDRESS_LINE_1_KEY]
        == ADDRESS_LINE_1_VALUE
    )
    assert (
        actual_structured_postal_address_user_profile[TOWN_CITY_KEY] == TOWN_CITY_VALUE
    )
    assert (
        actual_structured_postal_address_user_profile[POSTAL_CODE_KEY]
        == POSTAL_CODE_VALUE
    )
    assert (
        actual_structured_postal_address_user_profile[COUNTRY_ISO_KEY]
        == COUNTRY_ISO_VALUE
    )
    assert actual_structured_postal_address_user_profile[COUNTRY_KEY] == COUNTRY_VALUE

    assert (
        actual_structured_postal_address_user_profile[config.KEY_FORMATTED_ADDRESS]
        == formatted_address_json
    )


def test_set_address_to_be_formatted_address(successful_receipt):
    activity_details = ActivityDetails(successful_receipt)

    structured_postal_address = {config.KEY_FORMATTED_ADDRESS: FORMATTED_ADDRESS_VALUE}
    structured_postal_address_json = json.dumps(structured_postal_address)

    create_structured_postal_address_field(
        activity_details, structured_postal_address_json
    )
    activity_details.user_profile[
        config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS
    ] = ActivityDetails.try_convert_structured_postal_address_to_dict(
        activity_details.field
    )

    assert config.ATTRIBUTE_POSTAL_ADDRESS not in activity_details.user_profile

    ActivityDetails.ensure_postal_address(activity_details)

    assert (
        activity_details.user_profile[config.ATTRIBUTE_POSTAL_ADDRESS]
        == FORMATTED_ADDRESS_VALUE
    )
