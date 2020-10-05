import json
import unittest

from mock import Mock

from yoti_python_sdk.doc_scan.session.create import SessionSpecBuilder
from yoti_python_sdk.doc_scan.session.create.check.requested_check import RequestedCheck
from yoti_python_sdk.doc_scan.session.create.filter.required_id_document import (
    RequiredIdDocument,
)
from yoti_python_sdk.doc_scan.session.create.notification_config import (
    NotificationConfig,
)
from yoti_python_sdk.doc_scan.session.create.sdk_config import SdkConfig
from yoti_python_sdk.doc_scan.session.create.session_spec import SessionSpec
from yoti_python_sdk.doc_scan.session.create.task.requested_task import RequestedTask
from yoti_python_sdk.utils import YotiEncoder


class SessionSpecTest(unittest.TestCase):
    SOME_CLIENT_SESSION_TOKEN_TTL = 300
    SOME_RESOURCES_TTL = 100000
    SOME_USER_TRACKING_ID = "someUserTrackingId"

    def test_should_build_correctly(self):
        sdk_config_mock = Mock(spec=SdkConfig)
        notification_mock = Mock(spec=NotificationConfig)
        requested_check_mock = Mock(spec=RequestedCheck)
        requested_task_mock = Mock(spec=RequestedTask)

        result = (
            SessionSpecBuilder()
            .with_client_session_token_ttl(self.SOME_CLIENT_SESSION_TOKEN_TTL)
            .with_resources_ttl(self.SOME_RESOURCES_TTL)
            .with_user_tracking_id(self.SOME_USER_TRACKING_ID)
            .with_notifications(notification_mock)
            .with_sdk_config(sdk_config_mock)
            .with_requested_check(requested_check_mock)
            .with_requested_task(requested_task_mock)
            .build()
        )

        assert result.client_session_token_ttl is self.SOME_CLIENT_SESSION_TOKEN_TTL
        assert result.resources_ttl is self.SOME_RESOURCES_TTL
        assert result.user_tracking_id is self.SOME_USER_TRACKING_ID
        assert result.sdk_config is sdk_config_mock
        assert result.notifications is notification_mock
        assert len(result.requested_checks) == 1
        assert requested_check_mock in result.requested_checks
        assert len(result.requested_tasks) == 1
        assert requested_task_mock in result.requested_tasks

    def test_should_serialize_to_json_without_error(self):
        sdk_config_mock = Mock(spec=SdkConfig)
        sdk_config_mock.to_json.return_value = {}

        notification_mock = Mock(spec=NotificationConfig)
        notification_mock.to_json.return_value = {}

        requested_check_mock = Mock(spec=RequestedCheck)
        requested_check_mock.to_json.return_value = {}

        requested_task_mock = Mock(spec=RequestedTask)
        requested_task_mock.to_json.return_value = {}

        result = (
            SessionSpecBuilder()
            .with_client_session_token_ttl(self.SOME_CLIENT_SESSION_TOKEN_TTL)
            .with_resources_ttl(self.SOME_RESOURCES_TTL)
            .with_user_tracking_id(self.SOME_USER_TRACKING_ID)
            .with_notifications(notification_mock)
            .with_sdk_config(sdk_config_mock)
            .with_requested_check(requested_check_mock)
            .with_requested_task(requested_task_mock)
            .build()
        )

        s = json.dumps(result, cls=YotiEncoder)
        assert s is not None and s != ""

    def test_should_add_required_document(self):
        required_document_mock = Mock(spec=RequiredIdDocument)

        result = (
            SessionSpecBuilder().with_required_document(required_document_mock).build()
        )

        assert len(result.required_documents) == 1
        assert result.required_documents[0] == required_document_mock

    def test_should_default_empty_arrays(self):
        result = SessionSpec(
            client_session_token_ttl=1,
            resources_ttl=1,
            user_tracking_id="someTrackingId",
            notifications=None,
            sdk_config=None,
            requested_checks=None,
            requested_tasks=None,
            required_documents=None,
        )

        assert len(result.requested_checks) == 0
        assert len(result.requested_tasks) == 0
        assert len(result.required_documents) == 0

    def test_should_build_correctly_with_block_biometric_consent_true(self):
        result = SessionSpecBuilder().with_block_biometric_consent(True).build()

        assert result.block_biometric_consent is True

    def test_should_build_correctly_with_block_biometric_consent_false(self):
        result = SessionSpecBuilder().with_block_biometric_consent(False).build()

        assert result.block_biometric_consent is False

    def test_should_build_correctly_without_block_biometric_consent_false(self):
        result = SessionSpecBuilder().build()

        assert result.block_biometric_consent is None


if __name__ == "__main__":
    unittest.main()
