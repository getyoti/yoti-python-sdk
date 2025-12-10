import unittest

from yoti_python_sdk.doc_scan.session.retrieve.share_code_resource_response import (
    ShareCodeResourceResponse,
    ShareCodeProfile,
    ShareCodeIdPhoto,
    VerifyShareCodeTaskResponse,
)


class ShareCodeResourceResponseTest(unittest.TestCase):
    def test_should_parse_correctly(self):
        data = {
            "id": "some-id",
            "source": "some-source",
            "created_at": "2023-01-01T00:00:00Z",
            "last_updated": "2023-01-02T00:00:00Z",
            "lookup_profile": {
                "media": {
                    "id": "media-id-1",
                    "type": "JSON",
                    "created": "2023-01-01T00:00:00Z",
                    "last_updated": "2023-01-02T00:00:00Z",
                }
            },
            "returned_profile": {
                "media": {
                    "id": "media-id-2",
                    "type": "JSON",
                    "created": "2023-01-01T00:00:00Z",
                    "last_updated": "2023-01-02T00:00:00Z",
                }
            },
            "id_photo": {
                "media": {
                    "id": "media-id-3",
                    "type": "IMAGE",
                    "created": "2023-01-01T00:00:00Z",
                    "last_updated": "2023-01-02T00:00:00Z",
                }
            },
            "file": {
                "media": {
                    "id": "media-id-4",
                    "type": "JSON",
                    "created": "2023-01-01T00:00:00Z",
                    "last_updated": "2023-01-02T00:00:00Z",
                }
            },
            "tasks": [
                {
                    "type": "VERIFY_SHARE_CODE_TASK",
                    "id": "task-id-1",
                    "state": "DONE",
                    "created": "2023-01-01T00:00:00Z",
                    "last_updated": "2023-01-02T00:00:00Z",
                    "generated_media": [
                        {"id": "gen-media-1", "type": "JSON"}
                    ],
                }
            ],
        }

        result = ShareCodeResourceResponse(data)

        assert result.id == "some-id"
        assert result.source == "some-source"
        assert result.created_at == "2023-01-01T00:00:00Z"
        assert result.last_updated == "2023-01-02T00:00:00Z"
        assert result.lookup_profile is not None
        assert result.returned_profile is not None
        assert result.id_photo is not None
        assert result.file is not None
        assert len(result.tasks) == 1

    def test_should_parse_with_none(self):
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

    def test_should_parse_tasks(self):
        data = {
            "tasks": [
                {
                    "type": "VERIFY_SHARE_CODE_TASK",
                    "id": "task-id-1",
                    "state": "DONE",
                    "created": "2023-01-01T00:00:00Z",
                    "last_updated": "2023-01-02T00:00:00Z",
                    "generated_media": [],
                },
                {
                    "type": "VERIFY_SHARE_CODE_TASK",
                    "id": "task-id-2",
                    "state": "IN_PROGRESS",
                    "created": "2023-01-01T00:00:00Z",
                    "last_updated": "2023-01-02T00:00:00Z",
                    "generated_media": [],
                },
            ]
        }

        result = ShareCodeResourceResponse(data)

        assert len(result.tasks) == 2
        assert len(result.verify_share_code_tasks) == 2
        assert isinstance(result.tasks[0], VerifyShareCodeTaskResponse)
        assert result.tasks[0].type == "VERIFY_SHARE_CODE_TASK"
        assert result.tasks[0].id == "task-id-1"
        assert result.tasks[0].state == "DONE"


class ShareCodeProfileTest(unittest.TestCase):
    def test_should_parse_correctly(self):
        data = {
            "media": {
                "id": "media-id",
                "type": "JSON",
                "created": "2023-01-01T00:00:00Z",
                "last_updated": "2023-01-02T00:00:00Z",
            }
        }

        result = ShareCodeProfile(data)

        assert result.media is not None
        assert result.media.id == "media-id"
        assert result.media.type == "JSON"

    def test_should_parse_with_none(self):
        result = ShareCodeProfile(None)

        assert result.media is None


class ShareCodeIdPhotoTest(unittest.TestCase):
    def test_should_parse_correctly(self):
        data = {
            "media": {
                "id": "photo-media-id",
                "type": "IMAGE",
                "created": "2023-01-01T00:00:00Z",
                "last_updated": "2023-01-02T00:00:00Z",
            }
        }

        result = ShareCodeIdPhoto(data)

        assert result.media is not None
        assert result.media.id == "photo-media-id"
        assert result.media.type == "IMAGE"

    def test_should_parse_with_none(self):
        result = ShareCodeIdPhoto(None)

        assert result.media is None


class VerifyShareCodeTaskResponseTest(unittest.TestCase):
    def test_should_parse_correctly(self):
        data = {
            "type": "VERIFY_SHARE_CODE_TASK",
            "id": "task-id",
            "state": "DONE",
            "created": "2023-01-01T00:00:00Z",
            "last_updated": "2023-01-02T00:00:00Z",
            "generated_media": [
                {"id": "gen-media-1", "type": "JSON"},
                {"id": "gen-media-2", "type": "IMAGE"},
            ],
        }

        result = VerifyShareCodeTaskResponse(data)

        assert result.type == "VERIFY_SHARE_CODE_TASK"
        assert result.id == "task-id"
        assert result.state == "DONE"
        assert result.created is not None
        assert result.last_updated is not None
        assert len(result.generated_media) == 2

    def test_should_parse_with_none(self):
        result = VerifyShareCodeTaskResponse(None)

        assert result.type is None
        assert result.id is None
        assert result.state is None
        assert result.created is None
        assert result.last_updated is None
        assert len(result.generated_media) == 0

    def test_should_handle_invalid_date(self):
        data = {
            "created": "invalid-date",
            "last_updated": "also-invalid",
        }

        result = VerifyShareCodeTaskResponse(data)

        assert result.created is None
        assert result.last_updated is None


if __name__ == "__main__":
    unittest.main()
