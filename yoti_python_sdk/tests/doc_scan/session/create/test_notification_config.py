import json
import unittest

from yoti_python_sdk.doc_scan.session.create import NotificationConfigBuilder
from yoti_python_sdk.doc_scan.session.create.notification_config import (
    NotificationConfig,
)
from yoti_python_sdk.utils import YotiEncoder


class NotificationConfigTest(unittest.TestCase):
    SOME_AUTH_TOKEN = "someAuthToken"
    SOME_ENDPOINT = "someEndpoint"
    SOME_TOPIC = "someTopic"

    def test_should_build_correctly(self):
        result = (
            NotificationConfigBuilder()
            .with_auth_token(self.SOME_AUTH_TOKEN)
            .with_endpoint(self.SOME_ENDPOINT)
            .with_topic(self.SOME_TOPIC)
            .build()
        )

        assert isinstance(result, NotificationConfig)
        assert result.auth_token is self.SOME_AUTH_TOKEN
        assert result.endpoint is self.SOME_ENDPOINT
        assert self.SOME_TOPIC in result.topics

    def test_should_add_resource_update_topic(self):
        result = (
            NotificationConfigBuilder()
            .with_auth_token(self.SOME_AUTH_TOKEN)
            .with_endpoint(self.SOME_ENDPOINT)
            .for_resource_update()
            .build()
        )

        assert "RESOURCE_UPDATE" in result.topics

    def test_should_add_task_completion_topic(self):
        result = (
            NotificationConfigBuilder()
            .with_auth_token(self.SOME_AUTH_TOKEN)
            .with_endpoint(self.SOME_ENDPOINT)
            .for_task_completion()
            .build()
        )

        assert "TASK_COMPLETION" in result.topics

    def test_should_add_session_completion_topic(self):
        result = (
            NotificationConfigBuilder()
            .with_auth_token(self.SOME_AUTH_TOKEN)
            .with_endpoint(self.SOME_ENDPOINT)
            .for_session_completion()
            .build()
        )

        assert "SESSION_COMPLETION" in result.topics

    def test_should_add_check_completion_topic(self):
        result = (
            NotificationConfigBuilder()
            .with_auth_token(self.SOME_AUTH_TOKEN)
            .with_endpoint(self.SOME_ENDPOINT)
            .for_check_completion()
            .build()
        )

        assert "CHECK_COMPLETION" in result.topics

    def test_should_allow_multiple_topics(self):
        result = (
            NotificationConfigBuilder()
            .with_auth_token(self.SOME_AUTH_TOKEN)
            .with_endpoint(self.SOME_ENDPOINT)
            .for_resource_update()
            .for_task_completion()
            .for_session_completion()
            .for_check_completion()
            .build()
        )

        expected = [
            "RESOURCE_UPDATE",
            "TASK_COMPLETION",
            "SESSION_COMPLETION",
            "CHECK_COMPLETION",
        ]
        assert all(x in result.topics for x in expected)

    def test_should_store_unique_topics(self):
        result = (
            NotificationConfigBuilder()
            .with_auth_token(self.SOME_AUTH_TOKEN)
            .with_endpoint(self.SOME_ENDPOINT)
            .for_resource_update()
            .for_resource_update()
            .for_resource_update()
            .build()
        )

        assert len(result.topics) == 1

    def test_should_serialize_to_json_without_error(self):
        result = (
            NotificationConfigBuilder()
            .with_auth_token(self.SOME_AUTH_TOKEN)
            .with_endpoint(self.SOME_ENDPOINT)
            .for_resource_update()
            .for_task_completion()
            .for_session_completion()
            .for_check_completion()
            .build()
        )

        s = json.dumps(result, cls=YotiEncoder)
        assert s is not None and s != ""

    def test_topics_should_default_to_empty_list_if_none(self):
        result = NotificationConfig("someAuthToken", "someEndpoint", None)

        assert isinstance(result.topics, list)
        assert len(result.topics) == 0


if __name__ == "__main__":
    unittest.main()
