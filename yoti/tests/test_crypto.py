# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest


@pytest.mark.parametrize('invalid_token', [
    '',
    None,
    'some_invalid_token',
    True,
    123,
])
def test_decrypting_an_invalid_toke__should_not_be_allowed(invalid_token, crypto):
    with pytest.raises(ValueError):
        crypto.decrypt_token(invalid_token)


def test_given_proper_encrypted_token__decrypting_should_yield_decrypted_token(
        encrypted_request_token, decrypted_request_token, crypto):
    expected_token = decrypted_request_token
    decrypted_token = crypto.decrypt_token(encrypted_request_token).decode('utf-8')
    assert decrypted_token == expected_token

