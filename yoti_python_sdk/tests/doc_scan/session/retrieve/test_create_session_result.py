import unittest

from yoti_python_sdk.doc_scan.session.retrieve.create_session_result import (
    CreateSessionResult,
)


class CreateSessionResultTest(unittest.TestCase):
    SOME_CLIENT_SESSION_TOKEN_TTL = 300
    SOME_CLIENT_SESSION_TOKEN = "someClientSessionToken"
    SOME_SESSION_ID = "someSessionId"

    def test_should_build_correctly(self):
        data = {
            "client_session_token_ttl": self.SOME_CLIENT_SESSION_TOKEN_TTL,
            "client_session_token": self.SOME_CLIENT_SESSION_TOKEN,
            "session_id": self.SOME_SESSION_ID,
        }

        result = CreateSessionResult(data)

        assert result.client_session_token_ttl is self.SOME_CLIENT_SESSION_TOKEN_TTL
        assert result.client_session_token is self.SOME_CLIENT_SESSION_TOKEN
        assert result.session_id is self.SOME_SESSION_ID

    def test_should_parse_when_given_none(self):
        result = CreateSessionResult(None)

        assert result.client_session_token_ttl is None
        assert result.client_session_token is None
        assert result.session_id is None


if __name__ == "__main__":
    unittest.main()
