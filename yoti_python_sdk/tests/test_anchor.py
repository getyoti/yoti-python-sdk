# -*- coding: utf-8 -*-
import datetime

import yoti_python_sdk
from yoti_python_sdk import config
from yoti_python_sdk.tests import anchor_parser


def test_parse_anchors_driving_license():
    parsed_anchor = anchor_parser.get_driving_license_anchor()

    assert parsed_anchor.anchor_type == config.ANCHOR_SOURCE
    assert parsed_anchor.signed_timestamp == datetime.datetime(2018, 4, 11, 13, 13, 3, 923537)
    assert parsed_anchor.sub_type == ""
    assert parsed_anchor.value == "DRIVING_LICENCE"
    assert parsed_anchor.origin_server_certs.serial_number == int("46131813624213904216516051554755262812")


def test_parse_anchors_passport():
    parsed_anchor = anchor_parser.get_passport_anchor()

    assert parsed_anchor.anchor_type == config.ANCHOR_SOURCE
    assert parsed_anchor.signed_timestamp == datetime.datetime(2018, 4, 12, 14, 14, 32, 835537)
    assert parsed_anchor.sub_type == "OCR"
    assert parsed_anchor.value == "PASSPORT"
    assert parsed_anchor.origin_server_certs.serial_number == int("277870515583559162487099305254898397834")


def test_parse_yoti_admin():
    parsed_anchor = anchor_parser.get_yoti_admin_anchor()

    assert parsed_anchor.anchor_type == config.ANCHOR_VERIFIER
    assert parsed_anchor.signed_timestamp == datetime.datetime(2018, 4, 11, 13, 13, 4, 95238)
    assert parsed_anchor.sub_type == ""
    assert parsed_anchor.value == "YOTI_ADMIN"
    assert parsed_anchor.origin_server_certs.serial_number == int("256616937783084706710155170893983549581")


def test_anchor_returns_correct_default_values():
    anchor = yoti_python_sdk.anchor.Anchor()

    assert anchor.anchor_type == "Unknown"
    assert anchor.signed_timestamp is None
    assert anchor.sub_type == ""
    assert anchor.value == ""
    assert anchor.origin_server_certs is None
