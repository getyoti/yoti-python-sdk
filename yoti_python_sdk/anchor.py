import datetime
import logging

import OpenSSL
import asn1
import yoti_python_sdk.protobuf.compubapi_v1.SignedTimestamp_pb2 as compubapi
from OpenSSL import crypto

from yoti_python_sdk import config

UNKNOWN_EXTENSION = ""
SOURCE_EXTENSION = "1.3.6.1.4.1.47127.1.1.1"
VERIFIER_EXTENSION = "1.3.6.1.4.1.47127.1.1.2"

UNKNOWN_ANCHOR_TYPE = "Unknown"
UNKNOWN_ANCHOR_VALUE = ""


class Anchor:
    def __init__(
        self,
        anchor_type=None,
        sub_type=None,
        value=None,
        signed_timestamp=None,
        origin_server_certs=None,
    ):
        if sub_type is None:
            sub_type = ""

        if value is None:
            value = ""

        if anchor_type is None:
            anchor_type = UNKNOWN_ANCHOR_TYPE

        self.__anchor_type = anchor_type
        self.__sub_type = sub_type
        self.__value = value
        self.__signed_timestamp = signed_timestamp
        self.__origin_server_certs = origin_server_certs

    def __iter__(self):
        return self

    def __next__(self):
        self.idx += 1
        try:
            return self.data[self.idx - 1]
        except IndexError:
            self.idx = 0
            raise StopIteration

    next = __next__  # python2.x compatibility.

    @staticmethod
    def parse_anchors(anchors):
        if anchors is None:
            return None

        parsed_anchors = []
        for anc in anchors:
            if hasattr(anc, "origin_server_certs"):
                anchor_type = UNKNOWN_ANCHOR_TYPE
                try:
                    origin_server_certs_list = list(anc.origin_server_certs)
                    origin_server_certs_item = origin_server_certs_list[0]

                    crypto_cert = crypto.load_certificate(
                        OpenSSL.crypto.FILETYPE_ASN1, origin_server_certs_item
                    ).to_cryptography()

                except Exception as exc:
                    if logging.getLogger().propagate:
                        logging.warning(
                            "Error loading anchor certificate, exception: {0} - {1}".format(
                                type(exc).__name__, exc
                            )
                        )
                    continue

                has_found_anchor = False
                for i in range(len(crypto_cert.extensions)):
                    anchor_type = UNKNOWN_ANCHOR_TYPE

                    try:
                        extensions = crypto_cert.extensions[i]
                        if hasattr(extensions, "oid"):
                            oid = extensions.oid
                            if hasattr(oid, "dotted_string"):
                                if oid.dotted_string == SOURCE_EXTENSION:
                                    anchor_type = config.ANCHOR_SOURCE
                                elif oid.dotted_string == VERIFIER_EXTENSION:
                                    anchor_type = config.ANCHOR_VERIFIER

                                if anchor_type != UNKNOWN_ANCHOR_TYPE:
                                    has_found_anchor = True
                                    parsed_anchors = Anchor.get_values_from_extensions(
                                        anc,
                                        anchor_type,
                                        extensions,
                                        crypto_cert,
                                        parsed_anchors,
                                    )

                    except Exception as exc:
                        if logging.getLogger().propagate:
                            logging.warning(
                                "Error parsing anchor certificate extension, exception: {0} - {1}".format(
                                    type(exc).__name__, exc
                                )
                            )
                        continue

                if not has_found_anchor:
                    parsed_anchors.append(
                        Anchor(
                            UNKNOWN_ANCHOR_TYPE,
                            anc.sub_type,
                            UNKNOWN_ANCHOR_VALUE,
                            anc.signed_time_stamp,
                            crypto_cert,
                        )
                    )

        return parsed_anchors

    @staticmethod
    def get_values_from_extensions(
        anc, anchor_type, extensions, crypto_cert, parsed_anchors
    ):
        if hasattr(extensions, "value") and anchor_type != UNKNOWN_ANCHOR_TYPE:
            extension_value = ""
            if hasattr(extensions.value, "value"):
                extension_value = Anchor.decode_asn1_value(extensions.value.value)
            parsed_anchors.append(
                Anchor(
                    anchor_type,
                    anc.sub_type,
                    extension_value,
                    anc.signed_time_stamp,
                    crypto_cert,
                )
            )

        return parsed_anchors

    @staticmethod
    def decode_asn1_value(value_to_decode):
        extension_value_asn1 = value_to_decode
        decoder = asn1.Decoder()

        decoder.start(extension_value_asn1)
        tag, once_decoded_value = decoder.read()

        decoder.start(once_decoded_value)
        tag, twice_decoded_value = decoder.read()

        utf8_value = twice_decoded_value.decode("utf-8")
        return utf8_value

    @property
    def anchor_type(self):
        return self.__anchor_type

    @property
    def value(self):
        return self.__value

    @property
    def sub_type(self):
        return self.__sub_type

    @property
    def signed_timestamp(self):
        if self.__signed_timestamp is None:
            return None

        signed_timestamp_object = compubapi.SignedTimestamp()
        signed_timestamp_object.MergeFromString(self.__signed_timestamp)

        try:
            signed_timestamp_parsed = datetime.datetime.fromtimestamp(
                signed_timestamp_object.timestamp / float(1000000)
            )
        except OSError:
            print(
                "Unable to parse timestamp from integer: '{0}'".format(
                    signed_timestamp_object.timestamp
                )
            )
            return ""

        return signed_timestamp_parsed

    @property
    def origin_server_certs(self):
        return self.__origin_server_certs
