import unittest

from yoti_python_sdk.doc_scan.session.retrieve.resource_response import ResourceResponse
from yoti_python_sdk.doc_scan.session.retrieve.share_code_media_response import (
    ShareCodeMediaResponse,
)
from yoti_python_sdk.doc_scan.session.retrieve.share_code_resource_response import (
    ShareCodeResourceResponse,
)
from yoti_python_sdk.doc_scan.session.retrieve.verify_share_code_task_response import (
    VerifyShareCodeTaskResponse,
)


class ShareCodeResourceResponseTest(unittest.TestCase):
    SOME_ID = "share-code-123"
    SOME_SOURCE = "test-source"
    SOME_CREATED_AT = "2026-01-14T10:00:00Z"
    SOME_LAST_UPDATED = "2026-01-14T11:00:00Z"

    def test_should_be_instance_of_resource_response(self):
        result = ShareCodeResourceResponse({})

        assert isinstance(result, ResourceResponse)

    def test_should_parse_correctly(self):
        data = {
            "id": self.SOME_ID,
            "source": self.SOME_SOURCE,
            "created_at": self.SOME_CREATED_AT,
            "last_updated": self.SOME_LAST_UPDATED,
            "tasks": [],
        }

        result = ShareCodeResourceResponse(data)

        assert result.id == self.SOME_ID
        assert result.source == self.SOME_SOURCE
        assert result.created_at == self.SOME_CREATED_AT
        assert result.last_updated == self.SOME_LAST_UPDATED

    def test_should_parse_source_as_object(self):
        data = {
            "id": self.SOME_ID,
            "source": {"type": "END_USER"},
            "tasks": [],
        }

        result = ShareCodeResourceResponse(data)

        assert result.source == "END_USER"

    def test_should_parse_source_object_without_type_key(self):
        data = {
            "id": self.SOME_ID,
            "source": {"unknown_key": "some_value"},
            "tasks": [],
        }

        result = ShareCodeResourceResponse(data)

        assert result.source is not None

    def test_should_parse_when_none(self):
        result = ShareCodeResourceResponse(None)

        assert result.id is None
        assert result.source is None
        assert result.created_at is None
        assert result.last_updated is None
        assert result.lookup_profile is None
        assert result.returned_profile is None
        assert result.id_photo is None
        assert result.file is None
        assert len(result.tasks) == 0

    def test_should_parse_media_fields(self):
        data = {
            "id": self.SOME_ID,
            "lookup_profile": {"media": {"id": "media-1", "type": "JSON"}},
            "returned_profile": {"media": {"id": "media-2", "type": "JSON"}},
            "id_photo": {"media": {"id": "media-3", "type": "IMAGE"}},
            "file": {"media": {"id": "media-4", "type": "PDF"}},
            "tasks": [],
        }

        result = ShareCodeResourceResponse(data)

        assert isinstance(result.lookup_profile, ShareCodeMediaResponse)
        assert result.lookup_profile.media.id == "media-1"
        assert result.lookup_profile.media.type == "JSON"
        assert isinstance(result.returned_profile, ShareCodeMediaResponse)
        assert result.returned_profile.media.id == "media-2"
        assert isinstance(result.id_photo, ShareCodeMediaResponse)
        assert result.id_photo.media.id == "media-3"
        assert result.id_photo.media.type == "IMAGE"
        assert isinstance(result.file, ShareCodeMediaResponse)
        assert result.file.media.id == "media-4"
        assert result.file.media.type == "PDF"

    def test_should_return_none_for_null_media_fields(self):
        data = {
            "id": self.SOME_ID,
            "lookup_profile": None,
            "returned_profile": None,
            "id_photo": None,
            "file": None,
            "tasks": [],
        }

        result = ShareCodeResourceResponse(data)

        assert result.lookup_profile is None
        assert result.returned_profile is None
        assert result.id_photo is None
        assert result.file is None

    def test_should_return_none_for_missing_media_fields(self):
        result = ShareCodeResourceResponse({"tasks": []})

        assert result.lookup_profile is None
        assert result.returned_profile is None
        assert result.id_photo is None
        assert result.file is None

    def test_should_parse_verify_share_code_tasks(self):
        data = {
            "id": self.SOME_ID,
            "tasks": [
                {"type": "VERIFY_SHARE_CODE_TASK", "id": "task-1", "state": "DONE"},
            ],
        }

        result = ShareCodeResourceResponse(data)

        assert len(result.tasks) == 1
        assert len(result.verify_share_code_tasks) == 1
        assert isinstance(result.verify_share_code_tasks[0], VerifyShareCodeTaskResponse)

    def test_should_filter_verify_share_code_tasks(self):
        data = {
            "id": self.SOME_ID,
            "tasks": [
                {"type": "VERIFY_SHARE_CODE_TASK", "id": "task-verify", "state": "DONE"},
                {"type": "OTHER_TASK_TYPE", "id": "task-other", "state": "PENDING"},
            ],
        }

        result = ShareCodeResourceResponse(data)

        assert len(result.tasks) == 2
        assert len(result.verify_share_code_tasks) == 1
        assert result.verify_share_code_tasks[0].id == "task-verify"

    def test_should_parse_multiple_verify_share_code_tasks(self):
        data = {
            "id": self.SOME_ID,
            "tasks": [
                {"type": "VERIFY_SHARE_CODE_TASK", "id": "task-1", "state": "PENDING"},
                {"type": "VERIFY_SHARE_CODE_TASK", "id": "task-2", "state": "DONE"},
            ],
        }

        result = ShareCodeResourceResponse(data)

        assert len(result.verify_share_code_tasks) == 2
        assert result.verify_share_code_tasks[0].id == "task-1"
        assert result.verify_share_code_tasks[1].id == "task-2"

    def test_should_parse_full_realistic_payload(self):
        data = {
            "id": "abc12345-6789-abcd-ef01-234567890abc",
            "source": "END_USER",
            "created_at": "2026-02-05T11:33:46Z",
            "last_updated": "2026-02-05T11:33:50Z",
            "lookup_profile": {
                "media": {
                    "id": "df419a66-0449-41cf-a795-6dfaa993d1f6",
                    "type": "JSON",
                    "created": "2026-02-05T11:33:46Z",
                    "last_updated": "2026-02-05T11:33:50Z",
                }
            },
            "returned_profile": {
                "media": {
                    "id": "f2152059-2868-47c9-8f5f-64966c1b66b0",
                    "type": "JSON",
                    "created": "2026-02-05T11:33:46Z",
                    "last_updated": "2026-02-05T11:33:50Z",
                }
            },
            "id_photo": {
                "media": {
                    "id": "45e4ee9d-a77b-4007-afe9-ab7067687aff",
                    "type": "IMAGE",
                    "created": "2026-02-05T11:33:46Z",
                    "last_updated": "2026-02-05T11:33:50Z",
                }
            },
            "file": {
                "media": {
                    "id": "c83a9f12-1234-5678-9abc-def012345678",
                    "type": "PDF",
                    "created": "2026-02-05T11:33:46Z",
                    "last_updated": "2026-02-05T11:33:50Z",
                }
            },
            "tasks": [
                {
                    "type": "VERIFY_SHARE_CODE_TASK",
                    "id": "73141aa9-a01f-4de9-9281-1b11cda7ab75",
                    "state": "DONE",
                    "created": "2026-02-05T11:33:46Z",
                    "last_updated": "2026-02-05T11:33:50Z",
                    "generated_media": [
                        {"id": "df419a66-0449-41cf-a795-6dfaa993d1f6", "type": "PDF"},
                        {"id": "45e4ee9d-a77b-4007-afe9-ab7067687aff", "type": "IMAGE"},
                        {"id": "f2152059-2868-47c9-8f5f-64966c1b66b0", "type": "JSON"},
                    ],
                }
            ],
        }

        result = ShareCodeResourceResponse(data)

        assert result.id == "abc12345-6789-abcd-ef01-234567890abc"
        assert result.source == "END_USER"
        assert result.lookup_profile.media.id == "df419a66-0449-41cf-a795-6dfaa993d1f6"
        assert result.lookup_profile.media.type == "JSON"
        assert result.returned_profile.media.id == "f2152059-2868-47c9-8f5f-64966c1b66b0"
        assert result.id_photo.media.id == "45e4ee9d-a77b-4007-afe9-ab7067687aff"
        assert result.id_photo.media.type == "IMAGE"
        assert result.file.media.id == "c83a9f12-1234-5678-9abc-def012345678"
        assert result.file.media.type == "PDF"
        assert len(result.verify_share_code_tasks) == 1
        assert result.verify_share_code_tasks[0].state == "DONE"
        assert len(result.verify_share_code_tasks[0].generated_media) == 3


if __name__ == "__main__":
    unittest.main()
