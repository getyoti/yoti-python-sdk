# -*- coding: utf-8 -*-

import os.path
from yoti_python_sdk.tests import file_helper
from yoti_python_sdk.issuance_details import IssuanceDetails
from yoti_python_sdk.protobuf.share_public_api import ThirdPartyAttribute_pb2
from datetime import datetime

FIXTURES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")
THIRD_PARTY_ATTRIBUTE = os.path.join(FIXTURES_DIR, "testthirdpartyattribute.txt")


def test_should_parse_third_party_attribute_correctly():
    thirdparty_attribute_bytes = file_helper.get_file_bytes(THIRD_PARTY_ATTRIBUTE)

    proto = ThirdPartyAttribute_pb2.ThirdPartyAttribute()
    proto.MergeFromString(thirdparty_attribute_bytes)

    issuance_details = IssuanceDetails(proto)

    assert issuance_details.attributes[0].name == "com.thirdparty.id"
    assert issuance_details.token == "someIssuanceToken"
    assert issuance_details.expiry_date == datetime(2019, 10, 15, 22, 4, 5, 123000)
