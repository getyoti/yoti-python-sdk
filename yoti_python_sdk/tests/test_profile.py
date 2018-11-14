# -*- coding: utf-8 -*-
import collections
import json

from yoti_python_sdk import config
from yoti_python_sdk.profile import Profile
from yoti_python_sdk.protobuf.v1.protobuf import Protobuf
from yoti_python_sdk.tests.protobuf_attribute import ProtobufAttribute

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
INDIA_FORMATTED_ADDRESS_VALUE = 'S/O: Name\nHouse No.1111-A\n42nd Street\nTOWN/CITY NAME\nSub-DISTRICT 10\nDISTRICT 10\nPunjab\n141012\nRajgura Nagar\nIndia'
USA_FORMATTED_ADDRESS_VALUE = "15a North Street\nTOWN/CITY NAME\nAL\n36201\nUSA"


def create_single_attribute_list(name, value, anchors, content_type):
    attribute = ProtobufAttribute(name, value, anchors, content_type)

    attribute_list = list()
    attribute_list.append(attribute)
    return attribute_list


def create_attribute_list_with_selfie_field():
    return create_single_attribute_list(
        name=config.ATTRIBUTE_SELFIE,
        value="base64(ง •̀_•́)ง",
        anchors=None,
        content_type=Protobuf.CT_JPEG)


def create_attribute_list_with_email_field():
    return create_single_attribute_list(
        name=config.ATTRIBUTE_EMAIL_ADDRESS,
        value="y@ti.com".encode(),
        anchors=None,
        content_type=Protobuf.CT_STRING)


def create_attribute_list_with_structured_postal_address_field(json_address_value):
    return create_single_attribute_list(
        name=config.ATTRIBUTE_STRUCTURED_POSTAL_ADDRESS,
        value=json_address_value,
        anchors=None,
        content_type=Protobuf.CT_JSON)


def test_try_parse_structured_postal_address_uk():
    structured_postal_address = {ADDRESS_FORMAT_KEY: ADDRESS_FORMAT_VALUE,
                                 BUILDING_NUMBER_KEY: BUILDING_NUMBER_VALUE,
                                 ADDRESS_LINE_1_KEY: ADDRESS_LINE_1_VALUE,
                                 TOWN_CITY_KEY: TOWN_CITY_VALUE,
                                 POSTAL_CODE_KEY: POSTAL_CODE_VALUE,
                                 COUNTRY_ISO_KEY: COUNTRY_ISO_VALUE,
                                 COUNTRY_KEY: COUNTRY_VALUE,
                                 config.KEY_FORMATTED_ADDRESS: FORMATTED_ADDRESS_VALUE}

    structured_postal_address_json = json.dumps(structured_postal_address).encode()

    profile = Profile(create_attribute_list_with_structured_postal_address_field(structured_postal_address_json))

    actual_structured_postal_address_profile = profile.structured_postal_address.value

    assert type(actual_structured_postal_address_profile) is collections.OrderedDict
    assert actual_structured_postal_address_profile[ADDRESS_FORMAT_KEY] == ADDRESS_FORMAT_VALUE
    assert actual_structured_postal_address_profile[BUILDING_NUMBER_KEY] == BUILDING_NUMBER_VALUE
    assert actual_structured_postal_address_profile[ADDRESS_LINE_1_KEY] == ADDRESS_LINE_1_VALUE
    assert actual_structured_postal_address_profile[TOWN_CITY_KEY] == TOWN_CITY_VALUE
    assert actual_structured_postal_address_profile[POSTAL_CODE_KEY] == POSTAL_CODE_VALUE
    assert actual_structured_postal_address_profile[COUNTRY_ISO_KEY] == COUNTRY_ISO_VALUE
    assert actual_structured_postal_address_profile[COUNTRY_KEY] == COUNTRY_VALUE
    assert actual_structured_postal_address_profile[config.KEY_FORMATTED_ADDRESS] == FORMATTED_ADDRESS_VALUE


def test_try_parse_structured_postal_address_india():
    structured_postal_address = {ADDRESS_FORMAT_KEY: INDIA_FORMAT_VALUE,
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
                                 config.KEY_FORMATTED_ADDRESS: INDIA_FORMATTED_ADDRESS_VALUE}

    structured_postal_address_bytes = json.dumps(structured_postal_address).encode()

    profile = Profile(create_attribute_list_with_structured_postal_address_field(structured_postal_address_bytes))

    actual_structured_postal_address_profile = profile.structured_postal_address.value

    assert type(actual_structured_postal_address_profile) is collections.OrderedDict
    assert actual_structured_postal_address_profile[ADDRESS_FORMAT_KEY] == INDIA_FORMAT_VALUE
    assert actual_structured_postal_address_profile[CARE_OF_KEY] == CARE_OF_VALUE
    assert actual_structured_postal_address_profile[BUILDING_KEY] == BUILDING_VALUE
    assert actual_structured_postal_address_profile[STREET_KEY] == STREET_VALUE
    assert actual_structured_postal_address_profile[TOWN_CITY_KEY] == TOWN_CITY_VALUE
    assert actual_structured_postal_address_profile[SUBDISTRICT_KEY] == SUBDISTRICT_VALUE
    assert actual_structured_postal_address_profile[DISTRICT_KEY] == DISTRICT_VALUE
    assert actual_structured_postal_address_profile[STATE_KEY] == INDIA_STATE_VALUE
    assert actual_structured_postal_address_profile[POSTAL_CODE_KEY] == INDIA_POSTAL_CODE_VALUE
    assert actual_structured_postal_address_profile[POST_OFFICE_KEY] == INDIA_POST_OFFICE_VALUE
    assert actual_structured_postal_address_profile[COUNTRY_ISO_KEY] == INDIA_COUNTRY_ISO_VALUE
    assert actual_structured_postal_address_profile[COUNTRY_KEY] == INDIA_COUNTRY_VALUE
    assert actual_structured_postal_address_profile[config.KEY_FORMATTED_ADDRESS] == INDIA_FORMATTED_ADDRESS_VALUE


def test_try_parse_structured_postal_address_usa():
    structured_postal_address = {ADDRESS_FORMAT_KEY: USA_FORMAT_VALUE,
                                 ADDRESS_LINE_1_KEY: ADDRESS_LINE_1_VALUE,
                                 TOWN_CITY_KEY: TOWN_CITY_VALUE,
                                 STATE_KEY: USA_STATE_VALUE,
                                 POSTAL_CODE_KEY: USA_POSTAL_CODE_VALUE,
                                 COUNTRY_ISO_KEY: USA_COUNTRY_ISO_VALUE,
                                 COUNTRY_KEY: USA_COUNTRY_VALUE,
                                 config.KEY_FORMATTED_ADDRESS: USA_FORMATTED_ADDRESS_VALUE}

    structured_postal_address_bytes = json.dumps(structured_postal_address).encode()

    profile = Profile(create_attribute_list_with_structured_postal_address_field(structured_postal_address_bytes))

    actual_structured_postal_address_profile = profile.structured_postal_address.value

    assert type(actual_structured_postal_address_profile) is collections.OrderedDict
    assert actual_structured_postal_address_profile[ADDRESS_FORMAT_KEY] == USA_FORMAT_VALUE
    assert actual_structured_postal_address_profile[ADDRESS_LINE_1_KEY] == ADDRESS_LINE_1_VALUE
    assert actual_structured_postal_address_profile[TOWN_CITY_KEY] == TOWN_CITY_VALUE
    assert actual_structured_postal_address_profile[STATE_KEY] == USA_STATE_VALUE
    assert actual_structured_postal_address_profile[POSTAL_CODE_KEY] == USA_POSTAL_CODE_VALUE
    assert actual_structured_postal_address_profile[COUNTRY_ISO_KEY] == USA_COUNTRY_ISO_VALUE
    assert actual_structured_postal_address_profile[COUNTRY_KEY] == USA_COUNTRY_VALUE
    assert actual_structured_postal_address_profile[config.KEY_FORMATTED_ADDRESS] == USA_FORMATTED_ADDRESS_VALUE


def test_try_parse_structured_postal_address_nested_json():
    formatted_address_json = {
        "item1": [
            [1, 'a1'],
            [2, 'a2'],
        ],
        "item2": [
            [3, 'b3'],
            [4, 'b4'],
        ],
    }

    structured_postal_address = {ADDRESS_FORMAT_KEY: ADDRESS_FORMAT_VALUE,
                                 BUILDING_NUMBER_KEY: BUILDING_NUMBER_VALUE,
                                 ADDRESS_LINE_1_KEY: ADDRESS_LINE_1_VALUE,
                                 TOWN_CITY_KEY: TOWN_CITY_VALUE,
                                 POSTAL_CODE_KEY: POSTAL_CODE_VALUE,
                                 COUNTRY_ISO_KEY: COUNTRY_ISO_VALUE,
                                 COUNTRY_KEY: COUNTRY_VALUE,
                                 config.KEY_FORMATTED_ADDRESS: formatted_address_json}

    structured_postal_address_bytes = json.dumps(structured_postal_address).encode()

    profile = Profile(create_attribute_list_with_structured_postal_address_field(structured_postal_address_bytes))

    actual_structured_postal_address_profile = profile.structured_postal_address.value

    assert type(actual_structured_postal_address_profile) is collections.OrderedDict
    assert actual_structured_postal_address_profile[ADDRESS_FORMAT_KEY] == ADDRESS_FORMAT_VALUE
    assert actual_structured_postal_address_profile[BUILDING_NUMBER_KEY] == BUILDING_NUMBER_VALUE
    assert actual_structured_postal_address_profile[ADDRESS_LINE_1_KEY] == ADDRESS_LINE_1_VALUE
    assert actual_structured_postal_address_profile[TOWN_CITY_KEY] == TOWN_CITY_VALUE
    assert actual_structured_postal_address_profile[POSTAL_CODE_KEY] == POSTAL_CODE_VALUE
    assert actual_structured_postal_address_profile[COUNTRY_ISO_KEY] == COUNTRY_ISO_VALUE
    assert actual_structured_postal_address_profile[COUNTRY_KEY] == COUNTRY_VALUE

    assert actual_structured_postal_address_profile[config.KEY_FORMATTED_ADDRESS] == formatted_address_json


def test_set_address_to_be_formatted_address():
    structured_postal_address = {config.KEY_FORMATTED_ADDRESS: FORMATTED_ADDRESS_VALUE}
    structured_postal_address_bytes = json.dumps(structured_postal_address).encode()

    profile = Profile(create_attribute_list_with_structured_postal_address_field(structured_postal_address_bytes))

    assert profile.postal_address.value == FORMATTED_ADDRESS_VALUE


def test_get_attribute_selfie():
    profile = Profile(create_attribute_list_with_selfie_field())

    assert profile.get_attribute(config.ATTRIBUTE_SELFIE) == profile.selfie


def test_get_attribute_email_address():
    profile = Profile(create_attribute_list_with_email_field())

    assert profile.get_attribute(config.ATTRIBUTE_EMAIL_ADDRESS) == profile.email_address


def test_get_attribute_returns_none():
    profile = Profile(None)

    assert profile.get_attribute(config.ATTRIBUTE_SELFIE) is None
