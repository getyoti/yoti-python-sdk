# -*- coding: utf-8 -*-

import os.path
from yoti_python_sdk.tests import file_helper
from yoti_python_sdk.attribute_issuance_details import AttributeIssuanceDetails
from yoti_python_sdk.protobuf.share_public_api import ThirdPartyAttribute_pb2
from yoti_python_sdk.protobuf.share_public_api import IssuingAttributes_pb2
from datetime import datetime
import base64
import pytest

FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
THIRD_PARTY_ATTRIBUTE = os.path.join(FIXTURES_DIR, "testthirdpartyattribute.txt")


def create_issuance_test_proto(issuance_token, expiry_date, *definitions):
    issuing_attributes = IssuingAttributes_pb2.IssuingAttributes()
    issuing_attributes.expiry_date = expiry_date
    for s in definitions:
        name = IssuingAttributes_pb2.Definition()
        name.name = s
        issuing_attributes.definitions.extend([name])

    attribute = ThirdPartyAttribute_pb2.ThirdPartyAttribute()
    attribute.issuance_token = str(issuance_token).encode("utf-8")
    attribute.issuing_attributes.MergeFrom(issuing_attributes)
    return attribute


def test_should_parse_third_party_attribute_correctly():
    thirdparty_attribute_bytes = file_helper.get_file_bytes(THIRD_PARTY_ATTRIBUTE)

    proto = ThirdPartyAttribute_pb2.ThirdPartyAttribute()
    proto.MergeFromString(thirdparty_attribute_bytes)

    issuance_details = AttributeIssuanceDetails(proto)

    assert issuance_details.attributes[0].name == "com.thirdparty.id"
    assert issuance_details.token == base64.b64encode(
        "someIssuanceToken".encode("utf-8")
    )
    assert issuance_details.expiry_date == datetime(2019, 10, 15, 22, 4, 5, 123000)


@pytest.mark.parametrize(
    "expiry_date", ["2006-13-02T15:04:05.000Z", "", "2006-11-02T15:04:05"]
)
def test_should_return_none_if_error_in_parsing_date(expiry_date):
    proto = create_issuance_test_proto("someToken", expiry_date)

    issuance_details = AttributeIssuanceDetails(proto)

    assert issuance_details.expiry_date is None
