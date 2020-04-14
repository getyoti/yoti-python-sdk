import unittest

from yoti_python_sdk.doc_scan.session.retrieve.recommendation_response import (
    RecommendationResponse,
)


class RecommendationResponseTest(unittest.TestCase):
    SOME_VALUE = "someValue"
    SOME_REASON = "someReason"
    SOME_RECOVERY_SUGGESTION = "someRecoverySuggestion"

    def test_should_parse_correctly(self):
        data = {
            "value": self.SOME_VALUE,
            "reason": self.SOME_REASON,
            "recovery_suggestion": self.SOME_RECOVERY_SUGGESTION,
        }

        result = RecommendationResponse(data)

        assert result.value is self.SOME_VALUE
        assert result.reason is self.SOME_REASON
        assert result.recovery_suggestion is self.SOME_RECOVERY_SUGGESTION

    def test_should_parse_with_none(self):
        result = RecommendationResponse(None)

        assert result.value is None
        assert result.reason is None
        assert result.recovery_suggestion is None


if __name__ == "__main__":
    unittest.main()
