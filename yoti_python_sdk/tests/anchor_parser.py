import binascii
import io
from os.path import abspath, dirname, join

from yoti_python_sdk import anchor
from yoti_python_sdk.protobuf import protobuf

FIXTURES_DIR = join(dirname(abspath(__file__)), 'fixtures')
ANCHOR_DRIVING_LICENSE = join(FIXTURES_DIR, 'anchor_driving_license.txt')
ANCHOR_PASSPORT = join(FIXTURES_DIR, 'anchor_passport.txt')
ANCHOR_YOTI_ADMIN = join(FIXTURES_DIR, 'anchor_yoti_admin.txt')


def get_anchor_from_base64_text(file_path):
    base64_driving_license_anchor = read_file(file_path)
    driving_license_anchor_bytes = binascii.a2b_base64(base64_driving_license_anchor)

    protobuf_anchor = protobuf.Protobuf().anchor(driving_license_anchor_bytes)
    anchors = list()
    anchors.append(protobuf_anchor)

    return anchors


def get_parsed_driving_license_anchor():
    return anchor.Anchor().parse_anchors(get_anchor_from_base64_text(ANCHOR_DRIVING_LICENSE))[0]


def get_parsed_passport_anchor():
    return anchor.Anchor().parse_anchors(get_anchor_from_base64_text(ANCHOR_PASSPORT))[0]


def get_parsed_yoti_admin_anchor():
    return anchor.Anchor().parse_anchors(get_anchor_from_base64_text(ANCHOR_YOTI_ADMIN))[0]


def read_file(file_path):
    with io.open(file_path, mode='r', encoding='utf-8') as file:
        return file.read()
