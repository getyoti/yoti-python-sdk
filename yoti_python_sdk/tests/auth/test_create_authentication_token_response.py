from yoti_python_sdk.auth.create_authentication_token_response import (
    CreateAuthenticationTokenResponse,
)


def test_returns_all_properties():
    response = CreateAuthenticationTokenResponse(
        {
            "access_token": "someAccessToken",
            "token_type": "Bearer",
            "expires_in": 3600,
            "scope": "docscan.session.create",
        }
    )

    assert response.access_token == "someAccessToken"
    assert response.token_type == "Bearer"
    assert response.expires_in == 3600
    assert response.scope == "docscan.session.create"


def test_missing_properties_default_to_none():
    response = CreateAuthenticationTokenResponse({})

    assert response.access_token is None
    assert response.token_type is None
    assert response.expires_in is None
    assert response.scope is None
