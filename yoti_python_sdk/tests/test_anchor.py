# -*- coding: utf-8 -*-
import logging
import time
from datetime import datetime

from yoti_python_sdk.protobuf.attribute_public_api import Attribute_pb2

import yoti_python_sdk
from yoti_python_sdk import config
from yoti_python_sdk.anchor import Anchor
from yoti_python_sdk.tests import anchor_fixture_parser


def get_utc_offset():
    utc_offset = int(time.timezone / 60 / 60)

    if time.daylight:
        utc_offset = utc_offset - time.daylight

    return utc_offset


def test_parse_anchor_non_critical_only():
    parsed_anchor_list = anchor_fixture_parser.get_parsed_anchor_critical_last()

    assert len(parsed_anchor_list) == 1


def test_parse_anchors_driving_license():
    parsed_anchor = anchor_fixture_parser.get_parsed_driving_license_anchor()

    assert parsed_anchor.anchor_type == config.ANCHOR_SOURCE
    assert parsed_anchor.sub_type == ""
    assert parsed_anchor.value == "DRIVING_LICENCE"
    assert parsed_anchor.origin_server_certs.serial_number == int(
        "46131813624213904216516051554755262812"
    )
    assert parsed_anchor.signed_timestamp == datetime(
        2018, 4, 11, 12 - get_utc_offset(), 13, 3, 923537
    )


def test_parse_anchors_passport():
    parsed_anchor = anchor_fixture_parser.get_parsed_passport_anchor()

    assert parsed_anchor.anchor_type == config.ANCHOR_SOURCE
    assert parsed_anchor.sub_type == "OCR"
    assert parsed_anchor.value == "PASSPORT"
    assert parsed_anchor.origin_server_certs.serial_number == int(
        "277870515583559162487099305254898397834"
    )
    assert parsed_anchor.signed_timestamp == datetime(
        2018, 4, 12, 13 - get_utc_offset(), 14, 32, 835537
    )


def test_parse_yoti_admin():
    parsed_anchor = anchor_fixture_parser.get_parsed_yoti_admin_anchor()

    assert parsed_anchor.anchor_type == config.ANCHOR_VERIFIER
    assert parsed_anchor.sub_type == ""
    assert parsed_anchor.value == "YOTI_ADMIN"
    assert parsed_anchor.origin_server_certs.serial_number == int(
        "256616937783084706710155170893983549581"
    )
    assert parsed_anchor.signed_timestamp == datetime(
        2018, 4, 11, 12 - get_utc_offset(), 13, 4, 95238
    )


def test_anchor_returns_correct_default_values():
    default_anchor = yoti_python_sdk.anchor.Anchor()

    assert default_anchor.anchor_type == "Unknown"
    assert default_anchor.signed_timestamp is None
    assert default_anchor.sub_type == ""
    assert default_anchor.value == ""
    assert default_anchor.origin_server_certs is None


def test_error_parsing_anchor_certificate_carries_on_parsing():
    driving_license_anchor = anchor_fixture_parser.get_anchor_from_base64_text(
        anchor_fixture_parser.ANCHOR_DRIVING_LICENSE
    )[0]
    anchors = list()
    anchors.append(Attribute_pb2.Anchor())
    anchors.append(driving_license_anchor)

    # 1st anchor will log a warning when being parsed
    logger = logging.getLogger()
    logger.propagate = False

    parsed_anchors = Anchor.parse_anchors(anchors)
    logger.propagate = True

    assert len(parsed_anchors) == 1

    parsed_anchor = parsed_anchors[0]
    assert parsed_anchor.anchor_type == config.ANCHOR_SOURCE
    assert parsed_anchor.sub_type == ""
    assert parsed_anchor.value == "DRIVING_LICENCE"
    assert parsed_anchor.origin_server_certs.serial_number == int(
        "46131813624213904216516051554755262812"
    )
    assert parsed_anchor.signed_timestamp == datetime(
        2018, 4, 11, 12 - get_utc_offset(), 13, 3, 923537
    )


def test_processing_unknown_anchor_data():
    unknown_anchor_data = anchor_fixture_parser.get_anchor_from_base64_text(
        anchor_fixture_parser.ANCHOR_UNKNOWN_ANCHOR
    )
    anchors = Anchor.parse_anchors(unknown_anchor_data)

    assert len(anchors) == 1
    assert ("", "Unknown", "TEST UNKNOWN SUB TYPE") in [
        (anchor.value, anchor.anchor_type, anchor.sub_type) for anchor in anchors
    ]

    expected_timestamp = datetime(2019, 3, 5, 10, 45, 11, 840037)
    actual_timestamp = anchors[0].signed_timestamp

    assert expected_timestamp == actual_timestamp

    assert "document-registration-server" in [
        a.value for a in anchors[0].origin_server_certs.issuer
    ]
