import pytest
from yoti_python_sdk.digital_identity.create_share_qr_code_result import CreateShareQrCodeResult

def test_create_share_qr_code_result_with_data():
    # Arrange
    data = {
        'id': 'test_qr_code_id',
        'uri': 'https://example.com/qr_code_uri'
    }

    # Act
    result = CreateShareQrCodeResult(data)

    # Assert
    assert result.id == 'test_qr_code_id'
    assert result.uri == 'https://example.com/qr_code_uri'
    assert result.to_dict() == {
        'id': 'test_qr_code_id',
        'uri': 'https://example.com/qr_code_uri'
    }

def test_create_share_qr_code_result_without_data():
    # Act
    result = CreateShareQrCodeResult()

    # Assert
    assert result.id is None
    assert result.uri is None
    assert result.to_dict() == {
        'id': None,
        'uri': None
    }

def test_create_share_qr_code_result_partial_data():
    # Arrange
    data = {
        'id': 'test_qr_code_id'
        # uri is missing
    }

    # Act
    result = CreateShareQrCodeResult(data)

    # Assert
    assert result.id == 'test_qr_code_id'
    assert result.uri is None
    assert result.to_dict() == {
        'id': 'test_qr_code_id',
        'uri': None
    }
