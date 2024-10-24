import pytest
from yoti_python_sdk.digital_identity.get_share_session_result import GetShareSessionResult

def test_get_share_session_result_with_valid_data():
    # Arrange
    session_data = {
        'id': 'test_session_id',
        'status': 'active',
        'created': '2024-10-24T10:00:00Z',
        'updated': '2024-10-24T11:00:00Z',
        'expiry': '2024-10-24T12:00:00Z',
        'qrCode': {'id': 'test_qr_code_id'},
        'receipt': {'id': 'test_receipt_id'}
    }

    # Act
    session_result = GetShareSessionResult(session_data)

    # Assert
    assert session_result.id == 'test_session_id'
    assert session_result.status == 'active'
    assert session_result.created == '2024-10-24T10:00:00Z'
    assert session_result.updated == '2024-10-24T11:00:00Z'
    assert session_result.expiry == '2024-10-24T12:00:00Z'
    assert session_result.qrCode == {'id': 'test_qr_code_id'}
    assert session_result.receipt == {'id': 'test_receipt_id'}
    assert session_result.qrCodeId == 'test_qr_code_id'
    assert session_result.receiptId == 'test_receipt_id'
    assert session_result.to_dict() == session_data
