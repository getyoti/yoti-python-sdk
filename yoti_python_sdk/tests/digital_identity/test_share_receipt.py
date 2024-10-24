import pytest
from yoti_python_sdk.digital_identity.receipts.receipt_response import ReceiptResponse
from yoti_python_sdk.digital_identity.get_share_receipt_result import GetShareReceiptResult

def test_get_share_receipt_result_with_receipt_response_and_default_user_content():
    # Arrange
    receipt_data = {
        'id': 'test_receipt_id',
        'sessionId': 'test_session_id',
        'timestamp': '2024-10-24T10:00:00Z',
        'rememberMeId': 'test_remember_me_id',
        'parentRememberMeId': 'test_parent_remember_me_id'
    }
    receipt_response = ReceiptResponse(receipt_data)

    # Act
    result = GetShareReceiptResult(receipt_response)

    # Assert
    assert result.receiptId == 'test_receipt_id'
    assert result.sessionId == 'test_session_id'
    assert result.timestamp == '2024-10-24T10:00:00Z'
    assert result.rememberMeId == 'test_remember_me_id'
    assert result.parentRememberMeId == 'test_parent_remember_me_id'
    assert result.userContent is not None   
    assert result.to_dict() == {
        'id': 'test_receipt_id',
        'sessionId': 'test_session_id',
        'timestamp': '2024-10-24T10:00:00Z',
        'rememberMeId': 'test_remember_me_id',
        'parentRememberMeId': 'test_parent_remember_me_id'
    }
