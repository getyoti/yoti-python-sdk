# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from yoti_python_sdk.crypto import Crypto


@pytest.mark.parametrize("invalid_token", ["", None, "some_invalid_token", True, 123])
def test_decrypting_an_invalid_toke__should_not_be_allowed(invalid_token, crypto):
    with pytest.raises(ValueError):
        crypto.decrypt_token(invalid_token)


def test_given_proper_encrypted_token__decrypting_should_yield_decrypted_token(
    encrypted_request_token, decrypted_request_token, crypto
):
    expected_token = decrypted_request_token
    decrypted_token = crypto.decrypt_token(encrypted_request_token).decode("utf-8")
    assert decrypted_token == expected_token


@pytest.mark.parametrize(
    "with_padding,stripped",
    [
        (b"\xfa\x01", b"\xfa"),
        (b"\xfa\x06\x06\x06\x06\x06\x06", b"\xfa"),
        (b"\xfa\x08\x08\x08\x08\x08\x08\x08\x08", b"\xfa"),
    ],
)
def test_strip_pkcs5_padding(with_padding, stripped):
    assert Crypto.strip_pkcs5_padding(with_padding) == stripped


def test_sign_ps384_produces_a_verifiable_signature(crypto):
    message = b"some-message-to-sign"

    signature = crypto.sign_ps384(message)

    public_key = crypto.private_key.public_key()
    public_key.verify(
        signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA384()),
            salt_length=hashes.SHA384().digest_size,
        ),
        hashes.SHA384(),
    )


def test_sign_ps384_rejects_tampered_message(crypto):
    signature = crypto.sign_ps384(b"some-message-to-sign")

    public_key = crypto.private_key.public_key()
    with pytest.raises(InvalidSignature):
        public_key.verify(
            signature,
            b"some-other-message",
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA384()),
                salt_length=hashes.SHA384().digest_size,
            ),
            hashes.SHA384(),
        )
