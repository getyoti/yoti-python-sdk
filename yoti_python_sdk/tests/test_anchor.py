# -*- coding: utf-8 -*-
import binascii
import datetime
import io
from os.path import abspath, dirname, join

from yoti_python_sdk import anchor, config
from yoti_python_sdk.protobuf.v1 import protobuf

FIXTURES_DIR = join(dirname(abspath(__file__)), 'fixtures')
ANCHOR_DRIVING_LICENSE = join(FIXTURES_DIR, 'anchor_driving_license.txt')
ANCHOR_PASSPORT = join(FIXTURES_DIR, 'anchor_passport.txt')
ANCHOR_YOTI_ADMIN = join(FIXTURES_DIR, 'anchor_yoti_admin.txt')


def test_parse_anchors_driving_license():
    parsed_anchor = parse_anchor_from_text(ANCHOR_DRIVING_LICENSE)

    assert parsed_anchor.anchor_type == config.ANCHOR_SOURCE
    assert parsed_anchor.signed_timestamp == datetime.datetime(2018, 4, 11, 13, 13, 3, 923537)
    assert parsed_anchor.sub_type == ""
    assert parsed_anchor.value == "DRIVING_LICENCE"


def test_parse_anchors_passport():
    parsed_anchor = parse_anchor_from_text(ANCHOR_PASSPORT)

    assert parsed_anchor.anchor_type == config.ANCHOR_SOURCE
    assert parsed_anchor.signed_timestamp == datetime.datetime(2018, 4, 12, 14, 14, 32, 835537)
    assert parsed_anchor.sub_type == "OCR"
    assert parsed_anchor.value == "PASSPORT"


def test_parse_yoti_admin():
    parsed_anchor = parse_anchor_from_text(ANCHOR_YOTI_ADMIN)

    assert parsed_anchor.anchor_type == config.ANCHOR_VERIFIER
    assert parsed_anchor.signed_timestamp == datetime.datetime(2018, 4, 11, 13, 13, 4, 95238)
    assert parsed_anchor.sub_type == ""
    assert parsed_anchor.value == "YOTI_ADMIN"


def parse_anchor_from_text(file_path):
    base64_driving_license_anchor = read_file(file_path)
    driving_license_anchor_bytes = binascii.a2b_base64(base64_driving_license_anchor)

    protobuf_anchor = protobuf.Protobuf().anchor(driving_license_anchor_bytes)
    anchors = list()
    anchors.append(protobuf_anchor)

    return anchor.Anchor().parse_anchors(anchors)[0]


def read_file(file_path):
    with io.open(file_path, mode='r', encoding='utf-8') as file:
        return file.read()
