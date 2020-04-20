import unittest

from yoti_python_sdk.doc_scan.session.retrieve.check_response import (
    AuthenticityCheckResponse,
)
from yoti_python_sdk.doc_scan.session.retrieve.check_response import (
    FaceMatchCheckResponse,
)
from yoti_python_sdk.doc_scan.session.retrieve.check_response import (
    LivenessCheckResponse,
)
from yoti_python_sdk.doc_scan.session.retrieve.check_response import (
    TextDataCheckResponse,
)
from yoti_python_sdk.doc_scan.session.retrieve.get_session_result import (
    GetSessionResult,
)
from yoti_python_sdk.doc_scan.session.retrieve.resource_container import (
    ResourceContainer,
)


class GetSessionResultTest(unittest.TestCase):
    SOME_CLIENT_SESSION_TOKEN_TTL = 300
    SOME_SESSION_ID = "someSessionId"
    SOME_USER_TRACKING_ID = "someUserTrackingId"
    SOME_STATE = "someState"
    SOME_CLIENT_SESSION_TOKEN = "someClientSessionToken"
    SOME_CHECKS = [
        {"type": "ID_DOCUMENT_AUTHENTICITY"},
        {"type": "ID_DOCUMENT_TEXT_DATA_CHECK"},
        {"type": "ID_DOCUMENT_FACE_MATCH"},
        {"type": "LIVENESS"},
    ]

    def test_should_parse_different_checks(self):
        data = {
            "client_session_token_ttl": self.SOME_CLIENT_SESSION_TOKEN_TTL,
            "client_session_token": self.SOME_CLIENT_SESSION_TOKEN,
            "session_id": self.SOME_SESSION_ID,
            "state": self.SOME_STATE,
            "user_tracking_id": self.SOME_USER_TRACKING_ID,
            "checks": self.SOME_CHECKS,
            "resources": {},
        }

        result = GetSessionResult(data)

        assert result.client_session_token_ttl is self.SOME_CLIENT_SESSION_TOKEN_TTL
        assert result.client_session_token is self.SOME_CLIENT_SESSION_TOKEN
        assert result.session_id is self.SOME_SESSION_ID
        assert result.state is self.SOME_STATE
        assert result.user_tracking_id is self.SOME_USER_TRACKING_ID

        assert len(result.checks) == 4
        assert isinstance(result.checks[0], AuthenticityCheckResponse)
        assert isinstance(result.checks[1], TextDataCheckResponse)
        assert isinstance(result.checks[2], FaceMatchCheckResponse)
        assert isinstance(result.checks[3], LivenessCheckResponse)

        assert isinstance(result.resources, ResourceContainer)

    def test_should_filter_checks(self):
        data = {"checks": self.SOME_CHECKS}

        result = GetSessionResult(data)

        assert len(result.checks) == 4
        assert len(result.authenticity_checks) == 1
        assert len(result.face_match_checks) == 1
        assert len(result.liveness_checks) == 1
        assert len(result.text_data_checks) == 1


if __name__ == "__main__":
    unittest.main()
