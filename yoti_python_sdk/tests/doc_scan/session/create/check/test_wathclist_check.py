import json
import unittest

from yoti_python_sdk.doc_scan import constants
from yoti_python_sdk.doc_scan.session.create.check import (
    WatchlistScreeningCheckBuilder,
)
from yoti_python_sdk.doc_scan.session.create.check.requested_check import RequestedCheck
from yoti_python_sdk.doc_scan.session.create.check.watchlist_screen import (
    WatchlistScreeningCheck,
    WatchlistScreeningCheckConfig,
)
from yoti_python_sdk.utils import YotiEncoder
from yoti_python_sdk.doc_scan.constants import WATCHLIST_SCREENING_CHECK_TYPE


class WatchlistScreeningCheckTest(unittest.TestCase):
    def test_should_build_correctly_with_manual_check(self):
        dummy_manual_check = "DUMMY_VALUE"

        result = (
            WatchlistScreeningCheckBuilder()
            .with_manual_check(dummy_manual_check)
            .build()
        )

        assert isinstance(result, RequestedCheck)
        assert isinstance(result, WatchlistScreeningCheck)

        assert result.type == constants.WATCHLIST_SCREENING_CHECK_TYPE
        assert result.config.manual_check == dummy_manual_check
        assert result.config.categories == []

    def test_should_build_corretly_with_categories(self):
        dummy_categories = ["FIRST", "SECOND"]

        result = (
            WatchlistScreeningCheckBuilder()
            .with_categories(dummy_categories)
            .build()
        )

        assert isinstance(result, RequestedCheck)
        assert isinstance(result, WatchlistScreeningCheck)

        assert result.type == constants.WATCHLIST_SCREENING_CHECK_TYPE
        assert result.config.categories == dummy_categories
        assert result.config.manual_check is None

    def test_should_build_correctly_with_manual_check_and_categories(self):
        dummy_manual_check = "DUMMY_VALUE"
        dummy_categories = ["FIRST", "SECOND"]

        result = (
            WatchlistScreeningCheckBuilder()
            .with_manual_check(dummy_manual_check)
            .with_categories(dummy_categories)
            .build()
        )

        assert isinstance(result, RequestedCheck)
        assert isinstance(result, WatchlistScreeningCheck)

        assert result.type == constants.WATCHLIST_SCREENING_CHECK_TYPE
        assert result.config.manual_check == dummy_manual_check
        assert result.config.categories == dummy_categories

    def test_should_serialize_to_json_without_error(self):
        another_dummy_manual_check = "DUMMY_VALUE"
        another_dummy_categories = ["FIRST", "SECOND"]

        result = (
            WatchlistScreeningCheckBuilder()
            .with_manual_check(another_dummy_manual_check)
            .with_categories(another_dummy_categories)
            .build()
        )

        s = json.dumps(result, cls=YotiEncoder)
        assert s is not None and s != ""

        result = (
            WatchlistScreeningCheckBuilder()
            .with_categories(another_dummy_categories)
            .build()
        )

        s = json.dumps(result, cls=YotiEncoder)
        assert s is not None and s != ""

        s = json.loads(s)
        assert s.get("type") == WATCHLIST_SCREENING_CHECK_TYPE
        assert s.get("config") == {"categories": another_dummy_categories}

        result = (
            WatchlistScreeningCheckBuilder()
            .with_manual_check(another_dummy_manual_check)
            .build()
        )

        s = json.dumps(result, cls=YotiEncoder)
        assert s is not None and s != ""

        s = json.loads(s)
        assert s.get("type") == WATCHLIST_SCREENING_CHECK_TYPE
        assert s.get("config") == {"manual_check": "DUMMY_VALUE", "categories": []}
