import json
import unittest

from yoti_python_sdk.doc_scan import constants
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
    SOME_PRIVACY_POLICY_URL = "https://mysite.com/privacy"
    SOME_ALLOW_HANDOFF = True
    SOME_BRAND_ID = "your-brand-id"
    SOME_SUPPRESSED_SCREENS = [
        constants.ID_DOCUMENT_EDUCATION,
        constants.FLOW_COMPLETION,
    ]

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
            .with_privacy_policy_url(self.SOME_PRIVACY_POLICY_URL)
            .with_allow_handoff(self.SOME_ALLOW_HANDOFF)
            .with_brand_id(self.SOME_BRAND_ID)
            .with_suppressed_screens(self.SOME_SUPPRESSED_SCREENS)
            .build()
        )

        assert isinstance(result, SdkConfig)
        assert result.allowed_capture_methods == "CAMERA_AND_UPLOAD"
        assert result.primary_colour is self.SOME_PRIMARY_COLOUR
        assert result.secondary_colour is self.SOME_SECONDARY_COLOUR
        assert result.font_colour is self.SOME_FONT_COLOUR
        assert result.locale is self.SOME_LOCALE
        assert result.preset_issuing_country is self.SOME_PRESET_ISSUING_COUNTRY
        assert result.success_url == self.SOME_SUCCESS_URL
        assert result.error_url == self.SOME_ERROR_URL
        assert result.privacy_policy_url == self.SOME_PRIVACY_POLICY_URL
        assert result.allow_handoff is True
        assert result.brand_id == self.SOME_BRAND_ID
        assert result.suppressed_screens == self.SOME_SUPPRESSED_SCREENS

    def test_should_allows_camera(self):
        result = SdkConfigBuilder().with_allows_camera().build()

        assert result.allowed_capture_methods == "CAMERA"

    def test_not_passing_allow_handoff(self):
        result = SdkConfigBuilder().with_allows_camera().build()

        assert result.allow_handoff is None

    def test_passing_allow_handoff_false_value(self):
        result = SdkConfigBuilder().with_allow_handoff(False).build()

        assert result.allow_handoff is False

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
            .with_privacy_policy_url(self.SOME_PRIVACY_POLICY_URL)
            .build()
        )

        s = json.dumps(result, cls=YotiEncoder)
        assert s is not None and s != ""

    def test_not_passing_brand_id(self):
        result = SdkConfigBuilder().with_allows_camera().build()

        assert result.brand_id is None

    def test_with_brand_id(self):
        result = SdkConfigBuilder().with_brand_id(self.SOME_BRAND_ID).build()

        assert result.brand_id == self.SOME_BRAND_ID

    def test_brand_id_in_json_when_set(self):
        result = SdkConfigBuilder().with_brand_id(self.SOME_BRAND_ID).build()

        serialised = json.loads(json.dumps(result, cls=YotiEncoder))
        assert serialised["brand_id"] == self.SOME_BRAND_ID

    def test_brand_id_absent_from_json_when_not_set(self):
        result = SdkConfigBuilder().with_allows_camera().build()

        serialised = json.loads(json.dumps(result, cls=YotiEncoder))
        assert "brand_id" not in serialised

    def test_brand_id_absent_from_json_when_none(self):
        result = SdkConfigBuilder().with_brand_id(None).build()

        serialised = json.loads(json.dumps(result, cls=YotiEncoder))
        assert "brand_id" not in serialised

    def test_suppressed_screens_default_to_none(self):
        result = SdkConfigBuilder().with_allows_camera().build()

        assert result.suppressed_screens is None

    def test_should_add_individual_suppressed_screens(self):
        result = (
            SdkConfigBuilder()
            .with_suppressed_screen(constants.ID_DOCUMENT_EDUCATION)
            .with_suppressed_screen(constants.FLOW_COMPLETION)
            .build()
        )

        assert result.suppressed_screens == [
            constants.ID_DOCUMENT_EDUCATION,
            constants.FLOW_COMPLETION,
        ]

    def test_suppressed_screens_serialized_when_set(self):
        result = (
            SdkConfigBuilder()
            .with_suppressed_screens(self.SOME_SUPPRESSED_SCREENS)
            .build()
        )

        s = json.dumps(result, cls=YotiEncoder)
        parsed = json.loads(s)

        assert "suppressed_screens" in parsed
        assert parsed["suppressed_screens"] == self.SOME_SUPPRESSED_SCREENS

    def test_suppressed_screens_empty_list_serialized(self):
        result = SdkConfigBuilder().with_suppressed_screens([]).build()

        s = json.dumps(result, cls=YotiEncoder)
        parsed = json.loads(s)

        assert "suppressed_screens" in parsed
        assert parsed["suppressed_screens"] == []

    def test_suppressed_screens_omitted_when_not_set(self):
        result = SdkConfigBuilder().with_allows_camera().build()

        s = json.dumps(result, cls=YotiEncoder)
        parsed = json.loads(s)

        assert "suppressed_screens" not in parsed

    def test_with_suppressed_screens_returns_builder(self):
        builder = SdkConfigBuilder()
        result = builder.with_suppressed_screens(self.SOME_SUPPRESSED_SCREENS)

        assert result is builder

    def test_with_suppressed_screen_returns_builder(self):
        builder = SdkConfigBuilder()
        result = builder.with_suppressed_screen(constants.FLOW_COMPLETION)

        assert result is builder

    def test_suppressed_screen_constants_defined(self):
        assert constants.ID_DOCUMENT_EDUCATION == "ID_DOCUMENT_EDUCATION"
        assert constants.ID_DOCUMENT_REQUIREMENTS == "ID_DOCUMENT_REQUIREMENTS"
        assert (
            constants.SUPPLEMENTARY_DOCUMENT_EDUCATION
            == "SUPPLEMENTARY_DOCUMENT_EDUCATION"
        )
        assert constants.ZOOM_LIVENESS_EDUCATION == "ZOOM_LIVENESS_EDUCATION"
        assert constants.STATIC_LIVENESS_EDUCATION == "STATIC_LIVENESS_EDUCATION"
        assert constants.FACE_CAPTURE_EDUCATION == "FACE_CAPTURE_EDUCATION"
        assert constants.FLOW_COMPLETION == "FLOW_COMPLETION"


if __name__ == "__main__":
    unittest.main()
