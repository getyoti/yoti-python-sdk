# -*- coding: utf-8 -*-

from datetime import datetime
from types import SimpleNamespace

from yoti_python_sdk.share.extra_data import ExtraData


def create_third_party_test_data(token_value, expiry_date, *definitions):
    attribute = SimpleNamespace(
        issuance_token=bytes(token_value, "utf-8"),
        issuing_attributes=SimpleNamespace(
            expiry_date=expiry_date,
            definitions=[SimpleNamespace(name=s) for s in definitions],
        ),
    )
    return SimpleNamespace(type=ExtraData.THIRD_PARTY_ATTRIBUTE, value=attribute)


def test_attribute_issuance_details_should_return_nil_when_no_data_entries():
    extra_data = ExtraData([])

    assert extra_data.attribute_issuance_details is None


def test_should_return_first_matching_third_party_attribute():
    expiry_date = datetime.now()

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
