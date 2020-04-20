import unittest

from yoti_python_sdk.doc_scan.session.retrieve.recommendation_response import (
    RecommendationResponse,
)
from yoti_python_sdk.doc_scan.session.retrieve.report_response import ReportResponse


class ReportResponseTest(unittest.TestCase):
    def test_should_parse_correctly(self):
        data = {
            "recommendation": {"some": "recommendation"},
            "breakdown": [{"first": "breakdown"}, {"second": "breakdown"}],
        }

        result = ReportResponse(data)

        assert isinstance(result.recommendation, RecommendationResponse)
        assert len(result.breakdown) == 2

    def test_should_parse_with_none(self):
        result = ReportResponse(None)

        assert result.recommendation is None
        assert len(result.breakdown) == 0


if __name__ == "__main__":
    unittest.main()
