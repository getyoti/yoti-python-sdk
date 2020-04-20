import unittest

from yoti_python_sdk.doc_scan.session.retrieve.breakdown_response import (
    BreakdownResponse,
)


class BreakdownResponseTest(unittest.TestCase):
    SOME_SUB_CHECK = "someSubCheck"
    SOME_RESULT = "someResult"
    SOME_DETAILS = [
        {"name": "firstDetailName", "value": "firstDetailValue"},
        {"name": "secondDetailName", "value": "secondDetailValue"},
    ]

    def test_should_build_correctly(self):
        data = {
            "sub_check": self.SOME_SUB_CHECK,
            "result": self.SOME_RESULT,
            "details": self.SOME_DETAILS,
        }

        result = BreakdownResponse(data)

        assert result.sub_check is self.SOME_SUB_CHECK
        assert result.result is self.SOME_RESULT
        assert len(result.details) == 2
        assert result.details[0].name == "firstDetailName"
        assert result.details[0].value == "firstDetailValue"

    def test_should_default_details_to_empty_list(self):
        result = BreakdownResponse({})
        assert len(result.details) == 0


if __name__ == "__main__":
    unittest.main()
