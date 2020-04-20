import json
import unittest

from yoti_python_sdk.doc_scan.session.create import SdkConfigBuilder
from yoti_python_sdk.doc_scan.session.create.sdk_config import SdkConfig
from yoti_python_sdk.utils import YotiEncoder


class SdkConfigTest(unittest.TestCase):
    SOME_PRIMARY_COLOUR = "#77355f"
    SOME_SECONDARY_COLOUR = "#5bfc31"
    SOME_FONT_COLOUR = "#60f021"
    SOME_LOCALE = "en"
    SOME_PRESET_ISSUING_COUNTRY = "USA"
    SOME_SUCCESS_URL = "https://mysite.com/yoti/success"
    SOME_ERROR_URL = "https://mysite.com/yoti/error"

    def test_should_build_correctly(self):
        result = (
            SdkConfigBuilder()
            .with_allows_camera_and_upload()
            .with_primary_colour(self.SOME_PRIMARY_COLOUR)
            .with_secondary_colour(self.SOME_SECONDARY_COLOUR)
            .with_font_colour(self.SOME_FONT_COLOUR)
            .with_locale(self.SOME_LOCALE)
            .with_preset_issuing_country(self.SOME_PRESET_ISSUING_COUNTRY)
            .with_success_url(self.SOME_SUCCESS_URL)
            .with_error_url(self.SOME_ERROR_URL)
            .build()
        )

        assert isinstance(result, SdkConfig)
        assert result.allowed_capture_methods == "CAMERA_AND_UPLOAD"
        assert result.primary_colour is self.SOME_PRIMARY_COLOUR
        assert result.secondary_colour is self.SOME_SECONDARY_COLOUR
        assert result.font_colour is self.SOME_FONT_COLOUR
        assert result.locale is self.SOME_LOCALE
        assert result.preset_issuing_country is self.SOME_PRESET_ISSUING_COUNTRY
        assert result.success_url is self.SOME_SUCCESS_URL
        assert result.error_url is self.SOME_ERROR_URL

    def test_should_allows_camera(self):
        result = SdkConfigBuilder().with_allows_camera().build()

        assert result.allowed_capture_methods == "CAMERA"

    def test_should_serialize_to_json_without_error(self):
        result = (
            SdkConfigBuilder()
            .with_allows_camera_and_upload()
            .with_primary_colour(self.SOME_PRIMARY_COLOUR)
            .with_secondary_colour(self.SOME_SECONDARY_COLOUR)
            .with_font_colour(self.SOME_FONT_COLOUR)
            .with_locale(self.SOME_LOCALE)
            .with_preset_issuing_country(self.SOME_PRESET_ISSUING_COUNTRY)
            .with_success_url(self.SOME_SUCCESS_URL)
            .with_error_url(self.SOME_ERROR_URL)
            .build()
        )

        s = json.dumps(result, cls=YotiEncoder)
        assert s is not None and s != ""


if __name__ == "__main__":
    unittest.main()
