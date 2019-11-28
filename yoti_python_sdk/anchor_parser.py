import datetime
import logging

import pytz
import OpenSSL
import asn1
from OpenSSL import crypto

from yoti_python_sdk import config
from yoti_python_sdk.protobuf.common_public_api.SignedTimestamp_pb2 import (
    SignedTimestamp,
)
from yoti_python_sdk.anchor import (
    Anchor,
    SOURCE_EXTENSION,
    VERIFIER_EXTENSION,
    UNKNOWN_ANCHOR_VALUE,
)


def parse_anchors(anchors):
    """
    Parse the supplied anchors

    :return: tuple(Anchor, ...)
    """
    if anchors is None:
        return None

    parsed_anchors = []
    for anc in anchors:
        crypto_cert = extract_crypto_cert(anc)
        if crypto_cert is None:
            continue

        has_found_anchor = False
        for i in range(len(crypto_cert.extensions)):
            extension = crypto_cert.extensions[i]
            anchor_type = extract_anchor_type(extension)

            if (
                anchor_type == config.ANCHOR_SOURCE
                or anchor_type == config.ANCHOR_VERIFIER
            ):
                parsed_anchor = get_values_from_extensions(
                    anc, anchor_type, extension, crypto_cert
                )
                if parsed_anchor is not None:
                    has_found_anchor = True
                    parsed_anchors.append(parsed_anchor)

        if not has_found_anchor:
            parsed_anchors.append(
                Anchor(
                    config.ANCHOR_UNKNOWN,
                    anc.sub_type,
                    UNKNOWN_ANCHOR_VALUE,
                    parse_signed_timestamp(anc.signed_time_stamp),
                    crypto_cert,
                )
            )

    return tuple(parsed_anchors)


def extract_anchor_type(extension):
    try:
        if hasattr(extension, "oid"):
            oid = extension.oid
            if hasattr(oid, "dotted_string"):
                if oid.dotted_string == SOURCE_EXTENSION:
                    return config.ANCHOR_SOURCE
                elif oid.dotted_string == VERIFIER_EXTENSION:
                    return config.ANCHOR_VERIFIER
    except Exception as exc:
        if logging.getLogger().propagate:
            logging.warning(
                "Error parsing anchor certificate extension, exception: {0} - {1}".format(
                    type(exc).__name__, exc
                )
            )

    return config.ANCHOR_UNKNOWN


def extract_crypto_cert(anchor):
    if hasattr(anchor, "origin_server_certs"):
        try:
            origin_server_certs_list = list(anchor.origin_server_certs)
            origin_server_certs_item = origin_server_certs_list[0]

            crypto_cert = crypto.load_certificate(
                OpenSSL.crypto.FILETYPE_ASN1, origin_server_certs_item
            ).to_cryptography()

            return crypto_cert
        except Exception as exc:
            if logging.getLogger().propagate:
                logging.warning(
                    "Error loading anchor certificate, exception: {0} - {1}".format(
                        type(exc).__name__, exc
                    )
                )

    return None


def get_values_from_extensions(anc, anchor_type, extensions, crypto_cert):
    if hasattr(extensions, "value") and anchor_type != config.ANCHOR_UNKNOWN:
        extension_value = ""
        if hasattr(extensions.value, "value"):
            extension_value = decode_asn1_value(extensions.value.value)
        return Anchor(
            anchor_type,
            anc.sub_type,
            extension_value,
            parse_signed_timestamp(anc.signed_time_stamp),
            crypto_cert,
        )

    return None


def decode_asn1_value(value_to_decode):
    extension_value_asn1 = value_to_decode
    decoder = asn1.Decoder()

    decoder.start(extension_value_asn1)
    tag, once_decoded_value = decoder.read()

    decoder.start(once_decoded_value)
    tag, twice_decoded_value = decoder.read()

    utf8_value = twice_decoded_value.decode("utf-8")
    return utf8_value


def parse_signed_timestamp(timestamp):
    signed_timestamp_object = SignedTimestamp()
    signed_timestamp_object.MergeFromString(timestamp)

    try:
        signed_timestamp_parsed = datetime.datetime.fromtimestamp(
            signed_timestamp_object.timestamp / float(1000000), tz=pytz.utc
        )
    except OSError:
        print(
            "Unable to parse timestamp from integer: '{0}'".format(
                signed_timestamp_object.timestamp
            )
        )
        return None

    return signed_timestamp_parsed
