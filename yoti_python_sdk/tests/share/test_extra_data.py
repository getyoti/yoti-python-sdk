# -*- coding: utf-8 -*-

from datetime import datetime
import os.path
import base64

from yoti_python_sdk.share.extra_data import ExtraData
from yoti_python_sdk.tests import file_helper

from yoti_python_sdk.protobuf.share_public_api import IssuingAttributes_pb2
from yoti_python_sdk.protobuf.share_public_api import ThirdPartyAttribute_pb2
from yoti_python_sdk.protobuf.share_public_api import ExtraData_pb2
from yoti_python_sdk.protobuf.share_public_api import DataEntry_pb2

FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
EXTRADATA = os.path.join(FIXTURES_DIR, "testextradata.txt")


def create_third_party_test_data(token_value, expiry_date, *definitions):
    issuing_attributes = IssuingAttributes_pb2.IssuingAttributes()
    issuing_attributes.expiry_date = expiry_date
    for s in definitions:
        name = IssuingAttributes_pb2.Definition()
        name.name = s
        issuing_attributes.definitions.extend([name])

    attribute = ThirdPartyAttribute_pb2.ThirdPartyAttribute()
    attribute.issuance_token = token_value.encode("utf-8")
    attribute.issuing_attributes.MergeFrom(issuing_attributes)

    data_entry = DataEntry_pb2.DataEntry()
    data_entry.type = ExtraData.THIRD_PARTY_ATTRIBUTE
    data_entry.value = attribute.SerializeToString()

    return data_entry


def create_extra_data(data_entry_list):
    extra_data = ExtraData_pb2.ExtraData()
    extra_data.list.extend(data_entry_list)
    return extra_data.SerializeToString()


def get_extra_data_from_base64(filepath):
    extra_data_bytes = file_helper.get_file_bytes(filepath)

    return ExtraData(extra_data_bytes)


def test_attribute_issuance_details_should_return_none_when_no_data_entries():
    extra_data = ExtraData(create_extra_data([]))

    assert extra_data.attribute_issuance_details is None


def test_should_return_first_matching_third_party_attribute():
    expiry_date = datetime.now()

    thirdparty_attribute1 = create_third_party_test_data(
        "tokenValue1", expiry_date.isoformat(), "attributeName1"
    )
    thirdparty_attribute2 = create_third_party_test_data(
        "tokenValue2", expiry_date.isoformat(), "attributeName2"
    )

    parsed_extra_data = ExtraData(
        create_extra_data([thirdparty_attribute1, thirdparty_attribute2])
    )

    assert parsed_extra_data.attribute_issuance_details.token == base64.b64encode(
        "tokenValue1".encode("utf-8")
    )
    assert (
        parsed_extra_data.attribute_issuance_details.attributes[0].name
        == "attributeName1"
    )
    assert parsed_extra_data.attribute_issuance_details.expiry_date == expiry_date


def test_should_parse_multiple_issuing_attributes():
    extra_data = get_extra_data_from_base64(EXTRADATA)

    result = extra_data.attribute_issuance_details
    assert result is not None
    assert result.token == base64.b64encode("someIssuanceToken".encode("utf-8"))
    assert result.expiry_date == datetime(2019, 10, 15, 22, 4, 5, 123000)
    assert result.attributes[0].name == "com.thirdparty.id"
    assert result.attributes[1].name == "com.thirdparty.other_id"


def test_should_handle_no_expiry_date():
    tokenValue = "tokenValue"
    no_expiry = ""
    thirdparty_attribute = create_third_party_test_data(
        tokenValue, no_expiry, "attribute.name"
    )
    extra_data = ExtraData(create_extra_data([thirdparty_attribute]))

    result = extra_data.attribute_issuance_details
    assert result.expiry_date is None


def test_should_handle_no_issuing_attributes():
    tokenValue = "tokenValue"
    thirdparty_attribute = create_third_party_test_data(tokenValue, "")
    extra_data = ExtraData(create_extra_data([thirdparty_attribute]))

    result = extra_data.attribute_issuance_details
    assert result.token == base64.b64encode(tokenValue.encode("utf-8"))
    assert len(result.attributes) == 0


def test_should_handle_no_issuing_attribute_definitions():
    tokenValue = "tokenValue"
    expiry_date = datetime.now()
    thirdparty_attribute = create_third_party_test_data(
        tokenValue, expiry_date.isoformat()
    )
    extra_data = ExtraData(create_extra_data([thirdparty_attribute]))

    result = extra_data.attribute_issuance_details
    assert result.token == base64.b64encode(tokenValue.encode("utf-8"))
    assert result.expiry_date == expiry_date
    assert len(result.attributes) == 0
