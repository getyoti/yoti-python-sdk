# -*- coding: utf-8 -*-
from os.path import abspath, dirname, join

from yoti_python_sdk import anchor
from yoti_python_sdk.protobuf import protobuf
from yoti_python_sdk.tests import file_helper

FIXTURES_DIR = join(dirname(abspath(__file__)), "fixtures")
ANCHOR_DRIVING_LICENSE = join(FIXTURES_DIR, "anchor_driving_license.txt")
ANCHOR_PASSPORT = join(FIXTURES_DIR, "anchor_passport.txt")
ANCHOR_YOTI_ADMIN = join(FIXTURES_DIR, "anchor_yoti_admin.txt")
ANCHOR_UNKNOWN_ANCHOR = join(FIXTURES_DIR, "unknown_anchor.txt")
ANCHOR_CRITICAL_LAST = join(FIXTURES_DIR, "anchor_critical_last.txt")


def get_anchor_from_base64_text(file_path):
    anchor_bytes = file_helper.get_file_bytes(file_path)

    protobuf_anchor = protobuf.Protobuf().anchor(anchor_bytes)
    anchors = list()
    anchors.append(protobuf_anchor)

    return anchors


def get_parsed_driving_license_anchor():
    return anchor.Anchor().parse_anchors(
        get_anchor_from_base64_text(ANCHOR_DRIVING_LICENSE)
    )[0]


def get_parsed_anchor_critical_last():
    return anchor.Anchor().parse_anchors(
        get_anchor_from_base64_text(ANCHOR_CRITICAL_LAST)
    )


def get_parsed_passport_anchor():
    return anchor.Anchor().parse_anchors(get_anchor_from_base64_text(ANCHOR_PASSPORT))[
        0
    ]


def get_parsed_yoti_admin_anchor():
    return anchor.Anchor().parse_anchors(
        get_anchor_from_base64_text(ANCHOR_YOTI_ADMIN)
    )[0]
