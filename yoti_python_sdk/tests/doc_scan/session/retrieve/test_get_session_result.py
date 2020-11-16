import unittest

from datetime import datetime

import pytz

from yoti_python_sdk.doc_scan.session.retrieve.check_response import (
    AuthenticityCheckResponse,
    FaceMatchCheckResponse,
    LivenessCheckResponse,
    IDDocumentComparisonCheckResponse,
    TextDataCheckResponse,
    SupplementaryDocumentTextDataCheckResponse,
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
    SOME_BIOMETRIC_CONSENT = "2019-05-01T05:01:48.000Z"
    SOME_CHECKS = [
        {"type": "ID_DOCUMENT_AUTHENTICITY"},
        {"type": "ID_DOCUMENT_TEXT_DATA_CHECK"},
        {"type": "ID_DOCUMENT_FACE_MATCH"},
        {"type": "LIVENESS"},
        {"type": "ID_DOCUMENT_COMPARISON"},
        {"type": "SUPPLEMENTARY_DOCUMENT_TEXT_DATA_CHECK"},
    ]

    EXPECTED_BIOMETRIC_CONSENT_DATETIME = datetime(
        year=2019,
        month=5,
        day=1,
        hour=5,
        minute=1,
        second=48,
        microsecond=0,
        tzinfo=pytz.utc,
    )

    def test_should_parse_different_checks(self):
        data = {
            "client_session_token_ttl": self.SOME_CLIENT_SESSION_TOKEN_TTL,
            "client_session_token": self.SOME_CLIENT_SESSION_TOKEN,
            "session_id": self.SOME_SESSION_ID,
            "state": self.SOME_STATE,
            "user_tracking_id": self.SOME_USER_TRACKING_ID,
            "checks": self.SOME_CHECKS,
            "resources": {},
            "biometric_consent": self.SOME_BIOMETRIC_CONSENT,
        }

        result = GetSessionResult(data)

        assert result.client_session_token_ttl is self.SOME_CLIENT_SESSION_TOKEN_TTL
        assert result.client_session_token is self.SOME_CLIENT_SESSION_TOKEN
        assert result.session_id is self.SOME_SESSION_ID
        assert result.state is self.SOME_STATE
        assert result.user_tracking_id is self.SOME_USER_TRACKING_ID

        assert len(result.checks) == 6
        assert isinstance(result.checks[0], AuthenticityCheckResponse)
        assert isinstance(result.checks[1], TextDataCheckResponse)
        assert isinstance(result.checks[2], FaceMatchCheckResponse)
        assert isinstance(result.checks[3], LivenessCheckResponse)
        assert isinstance(result.checks[4], IDDocumentComparisonCheckResponse)
        assert isinstance(result.checks[5], SupplementaryDocumentTextDataCheckResponse)

        assert isinstance(result.resources, ResourceContainer)

        assert isinstance(result.biometric_consent_timestamp, datetime)
        assert (
            result.biometric_consent_timestamp
            == self.EXPECTED_BIOMETRIC_CONSENT_DATETIME
        )

    def test_should_filter_checks(self):
        data = {"checks": self.SOME_CHECKS}

        result = GetSessionResult(data)

        assert len(result.checks) == 6

        assert len(result.authenticity_checks) == 1
        assert isinstance(result.authenticity_checks[0], AuthenticityCheckResponse)

        assert len(result.face_match_checks) == 1
        assert isinstance(result.face_match_checks[0], FaceMatchCheckResponse)

        assert len(result.liveness_checks) == 1
        assert isinstance(result.liveness_checks[0], LivenessCheckResponse)

        assert len(result.text_data_checks) == 1
        assert isinstance(result.text_data_checks[0], TextDataCheckResponse)

        assert len(result.id_document_text_data_checks) == 1
        assert isinstance(result.id_document_text_data_checks[0], TextDataCheckResponse)

        assert len(result.id_document_comparison_checks) == 1
        assert isinstance(
            result.id_document_comparison_checks[0], IDDocumentComparisonCheckResponse
        )

        assert len(result.supplementary_document_text_data_checks) == 1
        assert isinstance(
            result.supplementary_document_text_data_checks[0],
            SupplementaryDocumentTextDataCheckResponse,
        )


if __name__ == "__main__":
    unittest.main()
