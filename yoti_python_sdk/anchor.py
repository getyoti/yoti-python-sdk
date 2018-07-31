import datetime

import OpenSSL
import asn1
from OpenSSL import crypto

import yoti_python_sdk.protobuf.v1.common_public_api.signed_timestamp_pb2 as compubapi
from yoti_python_sdk import config

UNKNOWN_EXTENSION = ""
SOURCE_EXTENSION = "1.3.6.1.4.1.47127.1.1.1"
VERIFIER_EXTENSION = "1.3.6.1.4.1.47127.1.1.2"


class Anchor:
    anchor_type = "Unknown"
    sub_type = ""
    value = ""
    signed_timestamp = compubapi.SignedTimestamp()

    def __init__(self, anchor_type=None, sub_type=None, value=None, signed_timestamp=None):
        self.anchor_type = anchor_type
        self.sub_type = sub_type
        self.value = value
        self.signed_timestamp = signed_timestamp

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
        for anc in anchors:
            parsed_anchors = []

            if hasattr(anc, 'origin_server_certs'):
                origin_server_certs_list = list(anc.origin_server_certs)
                origin_server_certs_item = origin_server_certs_list[0]

                cert = crypto.load_certificate(OpenSSL.crypto.FILETYPE_ASN1, origin_server_certs_item).to_cryptography()

                for i in range(len(cert.extensions)):
                    extensions = cert.extensions[i]
                    if hasattr(extensions, 'oid'):
                        oid = extensions.oid
                        if hasattr(oid, 'dotted_string'):
                            if oid.dotted_string == SOURCE_EXTENSION:
                                anchor_type = config.ANCHOR_SOURCE
                            elif oid.dotted_string == VERIFIER_EXTENSION:
                                anchor_type = config.ANCHOR_VERIFIER
                            else:
                                continue

                            if hasattr(extensions, 'value'):
                                extension_value = extensions.value
                                if hasattr(extension_value, 'value'):
                                    parsed_anchors.append(Anchor(
                                        anchor_type,
                                        Anchor.get_sub_type(anc),
                                        Anchor.decode_asn1_value(extension_value.value),
                                        Anchor.get_signed_timestamp(anc)))

        return parsed_anchors

    @staticmethod
    def decode_asn1_value(value_to_decode):
        extension_value_asn1 = value_to_decode
        decoder = asn1.Decoder()

        decoder.start(extension_value_asn1)
        tag, once_decoded_value = decoder.read()

        decoder.start(once_decoded_value)
        tag, twice_decoded_value = decoder.read()

        utf8_value = twice_decoded_value.decode('utf-8')
        return utf8_value

    @staticmethod
    def get_sub_type(anchor):
        if hasattr(anchor, 'sub_type'):
            return anchor.sub_type
        else:
            return ""

    @staticmethod
    def get_signed_timestamp(anchor):
        if hasattr(anchor, 'signed_time_stamp'):
            signed_timestamp_object = compubapi.SignedTimestamp()
            signed_timestamp_object.MergeFromString(anchor.signed_time_stamp)

            try:
                signed_timestamp_parsed = datetime.datetime.fromtimestamp(
                    signed_timestamp_object.timestamp / float(1000000))
            except OSError:
                print("Unable to parse timestamp from integer: '{0}'".format(signed_timestamp_object.timestamp))
                return ""

            return signed_timestamp_parsed
        else:
            return ""
