import pytest
from yoti_python_sdk.digital_identity.get_share_qr_code_result import GetShareQrCodeResult

def test_get_share_qr_code_result_with_data():
    # Arrange
    data = {
        'id': 'test_qr_code_id',
        'expiry': '2024-12-31T23:59:59Z',
        'sessionId': 'test_session_id',
        'redirectUri': 'https://example.com'
    }

    # Act
    result = GetShareQrCodeResult(data)

    # Assert
    assert result.id == 'test_qr_code_id'
    assert result.expiry == '2024-12-31T23:59:59Z'
    assert result.sessionId == 'test_session_id'
    assert result.redirectUri == 'https://example.com'
    assert result.to_dict() == {
        'id': 'test_qr_code_id',
        'expiry': '2024-12-31T23:59:59Z',
        'sessionId': 'test_session_id',
        'redirectUri': 'https://example.com'
    }

def test_get_share_qr_code_result_without_data():
    # Act
    result = GetShareQrCodeResult()

    # Assert
    assert result.id is None
    assert result.expiry is None
    assert result.sessionId is None
    assert result.redirectUri is None
    assert result.to_dict() == {
        'id': None,
        'expiry': None,
        'sessionId': None,
        'redirectUri': None
    }

def test_get_share_qr_code_result_partial_data():
    # Arrange
    data = {
        'id': 'test_qr_code_id',
        'sessionId': 'test_session_id'
        # expiry and redirectUri are missing
    }

    # Act
    result = GetShareQrCodeResult(data)

    # Assert
    assert result.id == 'test_qr_code_id'
    assert result.expiry is None
    assert result.sessionId == 'test_session_id'
    assert result.redirectUri is None
    assert result.to_dict() == {
        'id': 'test_qr_code_id',
        'expiry': None,
        'sessionId': 'test_session_id',
        'redirectUri': None
    }
