# -*- coding: utf-8 -*-

from datetime import datetime
from types import SimpleNamespace
import os.path

from yoti_python_sdk.share.extra_data import ExtraData
from yoti_python_sdk.tests import file_helper
from yoti_python_sdk.protobuf import protobuf

FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
EXTRADATA = os.path.join(FIXTURES_DIR, "testextradata.txt")


def create_third_party_test_data(token_value, expiry_date, *definitions):
    attribute = SimpleNamespace(
        issuance_token=bytes(token_value, "utf-8"),
        issuing_attributes=SimpleNamespace(
            expiry_date=expiry_date,
            definitions=[SimpleNamespace(name=s) for s in definitions],
        ),
    )
    return SimpleNamespace(type=ExtraData.THIRD_PARTY_ATTRIBUTE, value=attribute)


def get_extra_data_from_base64(filepath):
    extra_data_bytes = file_helper.get_file_bytes(filepath)
    protobuf_extra_data = protobuf.Protobuf.extra_data(extra_data_bytes)
    return ExtraData(protobuf_extra_data.list)


def test_attribute_issuance_details_should_return_nil_when_no_data_entries():
    extra_data = ExtraData([])

    assert extra_data.attribute_issuance_details is None


def test_should_return_first_matching_third_party_attribute():
    expiry_date = datetime.now().isoformat()

    thirdparty_attribute1 = create_third_party_test_data(
        "tokenValue1", expiry_date, "attributeName1"
    )
    thirdparty_attribute2 = create_third_party_test_data(
        "tokenValue2", expiry_date, "attributeName2"
    )

    parsed_extra_data = ExtraData([thirdparty_attribute1, thirdparty_attribute2])

    assert parsed_extra_data.attribute_issuance_details.token == "tokenValue1"
    assert (
        parsed_extra_data.attribute_issuance_details.attributes[0].name
        == "attributeName1"
    )
    assert parsed_extra_data.attribute_issuance_details.expiry_date == expiry_date


def test_should_parse_multiple_issuing_attributes():
    extra_data = get_extra_data_from_base64(EXTRADATA)
    result = extra_data.attribute_issuance_details
    assert result is not None

    assert result.token == "someIssuanceToken"
    assert result.expiry_date == "2019-10-15T22:04:05.123Z"
    assert result.attributes[0].name == "com.thirdparty.id"
    assert result.attributes[1].name == "com.thirdparty.other_id"
