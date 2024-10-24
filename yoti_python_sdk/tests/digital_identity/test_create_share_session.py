import pytest
from yoti_python_sdk.digital_identity.create_share_session_result import CreateShareSessionResult

def test_create_share_session_result_with_data():
    # Arrange
    data = {
        'id': 'test_session_id',
        'status': 'ACTIVE',
        'expiry': '2024-12-31T23:59:59Z'
    }

    # Act
    result = CreateShareSessionResult(data)

    # Assert
    assert result.id == 'test_session_id'
    assert result.status == 'ACTIVE'
    assert result.expiry == '2024-12-31T23:59:59Z'
    assert result.to_dict() == {
        'id': 'test_session_id',
        'status': 'ACTIVE',
        'expiry': '2024-12-31T23:59:59Z'
    }

def test_create_share_session_result_without_data():
    # Act
    result = CreateShareSessionResult()

    # Assert
    assert result.id is None
    assert result.status is None
    assert result.expiry is None
    assert result.to_dict() == {
        'id': None,
        'status': None,
        'expiry': None
    }

def test_create_share_session_result_partial_data():
    # Arrange
    data = {
        'id': 'test_session_id',
        'status': 'ACTIVE'
        # expiry is missing
    }

    # Act
    result = CreateShareSessionResult(data)

    # Assert
    assert result.id == 'test_session_id'
    assert result.status == 'ACTIVE'
    assert result.expiry is None
    assert result.to_dict() == {
        'id': 'test_session_id',
        'status': 'ACTIVE',
        'expiry': None
    }
