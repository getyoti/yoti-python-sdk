# -*- coding: utf-8 -*-

from yoti_python_sdk.document_details import DocumentDetails

import datetime
import pytest


def test_exception_for_empty_data():
    DATA = ""

    with pytest.raises(ValueError) as exc:
        DocumentDetails(DATA)
        assert str(exc.value) == "Invalid value for DocumentDetails"


def test_exception_for_short_data():
    DATA = "PASS_CARD GBR"

    with pytest.raises(ValueError) as exc:
        DocumentDetails(DATA)
        assert str(exc.value) == "Invalid value for DocumentDetails"


def test_parse_3_words():
    DATA = "PASSPORT GBR 01234567"

    document = DocumentDetails(DATA)

    assert document.document_type == "PASSPORT"
    assert document.issuing_country == "GBR"
    assert document.document_number == "01234567"
    assert document.expiration_date is None
    assert document.issuing_authority is None


def test_parse_redacted_aadhaar():
    DATA = "AADHAAR IND ****1234"

    document = DocumentDetails(DATA)

    assert document.document_type == "AADHAAR"
    assert document.issuing_country == "IND"
    assert document.document_number == "****1234"
    assert document.expiration_date is None
    assert document.issuing_authority is None


@pytest.mark.parametrize(
    "details, expected_number",
    [
        ("type country **** - authority", "****"),
        (
            "type country ~!@#$%^&*()-_=+[]{}|;':,./<>? - authority",
            "~!@#$%^&*()-_=+[]{}|;':,./<>?",
        ),
        ('type country "" - authority', '""'),
        ("type country \\ - authority", "\\"),
        ('type country " - authority', '"'),
        ("type country '' - authority", "''"),
        ("type country ' - authority", "'"),
    ],
)
def test_parse_special_characters(details, expected_number):
    document = DocumentDetails(details)

    assert document.document_type == "type"
    assert document.document_number == expected_number


def test_parse_4_words():
    DATA = "DRIVING_LICENCE GBR 1234abc 2016-05-01"

    document = DocumentDetails(DATA)

    assert document.document_type == "DRIVING_LICENCE"
    assert document.issuing_country == "GBR"
    assert document.document_number == "1234abc"
    assert document.expiration_date == datetime.date(2016, 5, 1)
    assert document.issuing_authority is None


def test_parse_5_words():
    DATA = "DRIVING_LICENCE GBR 1234abc 2016-05-01 DVLA"

    document = DocumentDetails(DATA)

    assert document.document_type == "DRIVING_LICENCE"
    assert document.issuing_country == "GBR"
    assert document.document_number == "1234abc"
    assert document.expiration_date == datetime.date(2016, 5, 1)
    assert document.issuing_authority == "DVLA"


def test_parse_6_words():
    DATA = "DRIVING_LICENCE GBR 1234abc 2016-05-01 DVLA someThirdData"

    document = DocumentDetails(DATA)

    assert document.document_type == "DRIVING_LICENCE"
    assert document.issuing_country == "GBR"
    assert document.document_number == "1234abc"
    assert document.expiration_date == datetime.date(2016, 5, 1)
    assert document.issuing_authority == "DVLA"


def test_expiration_date_is_dash():
    DATA = "PASS_CARD GBR 22719564893 - CITIZENCARD"

    document = DocumentDetails(DATA)

    assert document.document_type == "PASS_CARD"
    assert document.issuing_country == "GBR"
    assert document.document_number == "22719564893"
    assert document.expiration_date is None
    assert document.issuing_authority == "CITIZENCARD"


def test_invalid_date():
    DATA = "PASSPORT GBR 1234abc X016-05-01"

    with pytest.raises(ValueError) as exc:
        DocumentDetails(DATA)
        assert str(exc.value) == "Invalid value for DocumentDetails"


def test_should_fail_with_double_space():
    DATA = "AADHAAR  IND ****1234"

    with pytest.raises(ValueError) as exc:
        DocumentDetails(DATA)
        assert str(exc.value) == "Invalid value for DocumentDetails"
