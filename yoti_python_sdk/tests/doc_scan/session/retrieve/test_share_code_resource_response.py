# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

from yoti_python_sdk.doc_scan.session.retrieve.resource_response import (
    ResourceResponse,
)
from yoti_python_sdk.doc_scan.session.retrieve.share_code_resource_response import (
    ShareCodeResourceResponse,
)
from yoti_python_sdk.doc_scan.session.retrieve.verify_share_code_task_response import (
    VerifyShareCodeTaskResponse,
)


class ShareCodeResourceResponseTest(unittest.TestCase):
    def test_should_parse_correctly(self):
        data = {
            "id": "some-id",
            "source": "END_USER",
            "created_at": "2026-02-05T11:33:46Z",
            "last_updated": "2026-02-05T11:33:50Z",
            "tasks": [],
        }

        result = ShareCodeResourceResponse(data)

        assert result.id == "some-id"
        assert result.source == "END_USER"
        assert result.created_at == "2026-02-05T11:33:46Z"
        assert result.last_updated == "2026-02-05T11:33:50Z"

    def test_should_be_instance_of_resource_response(self):
        result = ShareCodeResourceResponse({})

        assert isinstance(result, ResourceResponse)

    def test_should_filter_verify_share_code_tasks(self):
        data = {
            "tasks": [
                {"type": "VERIFY_SHARE_CODE_TASK", "id": "task-1"},
                {"type": "SOME_OTHER_TASK", "id": "task-2"},
            ]
        }

        result = ShareCodeResourceResponse(data)

        assert len(result.tasks) == 2
        assert len(result.verify_share_code_tasks) == 1
        assert result.verify_share_code_tasks[0].id == "task-1"

    def test_should_parse_multiple_verify_share_code_tasks(self):
        data = {
            "tasks": [
                {"type": "VERIFY_SHARE_CODE_TASK", "id": "task-1"},
                {"type": "VERIFY_SHARE_CODE_TASK", "id": "task-2"},
            ]
        }

        result = ShareCodeResourceResponse(data)

        assert len(result.verify_share_code_tasks) == 2

    def test_should_parse_media_fields(self):
        data = {
            "lookup_profile": {"media": {"id": "lp-media", "type": "JSON"}},
            "returned_profile": {"media": {"id": "rp-media", "type": "JSON"}},
            "id_photo": {"media": {"id": "ip-media", "type": "IMAGE"}},
            "file": {"media": {"id": "f-media", "type": "PDF"}},
            "tasks": [],
        }

        result = ShareCodeResourceResponse(data)

        assert result.lookup_profile is not None
        assert result.lookup_profile.media.id == "lp-media"
        assert result.lookup_profile.media.type == "JSON"
        assert result.returned_profile is not None
        assert result.returned_profile.media.id == "rp-media"
        assert result.id_photo is not None
        assert result.id_photo.media.id == "ip-media"
        assert result.id_photo.media.type == "IMAGE"
        assert result.file is not None
        assert result.file.media.id == "f-media"
        assert result.file.media.type == "PDF"

    def test_should_parse_source_as_object(self):
        data = {"source": {"type": "END_USER"}, "tasks": []}

        result = ShareCodeResourceResponse(data)

        assert result.source == "END_USER"

    def test_should_parse_source_as_string(self):
        data = {"source": "END_USER", "tasks": []}

        result = ShareCodeResourceResponse(data)

        assert result.source == "END_USER"

    def test_should_return_none_for_missing_media_fields(self):
        data = {"tasks": []}

        result = ShareCodeResourceResponse(data)

        assert result.lookup_profile is None
        assert result.returned_profile is None
        assert result.id_photo is None
        assert result.file is None

    def test_should_return_none_for_null_media_fields(self):
        data = {
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

    def test_should_parse_with_no_tasks(self):
        data = {"id": "some-id", "tasks": []}

        result = ShareCodeResourceResponse(data)

        assert len(result.verify_share_code_tasks) == 0

    def test_should_parse_full_realistic_payload(self):
        data = {
            "id": "abc12345-share-code-id",
            "source": {"type": "END_USER"},
            "created_at": "2026-02-05T11:33:46Z",
            "last_updated": "2026-02-05T11:33:50Z",
            "lookup_profile": {
                "media": {
                    "id": "lp-media-id",
                    "type": "JSON",
                    "created": "2026-02-05T11:33:46Z",
                    "last_updated": "2026-02-05T11:33:50Z",
                }
            },
            "returned_profile": {
                "media": {
                    "id": "rp-media-id",
                    "type": "JSON",
                }
            },
            "id_photo": {
                "media": {
                    "id": "ip-media-id",
                    "type": "IMAGE",
                }
            },
            "file": {
                "media": {
                    "id": "f-media-id",
                    "type": "PDF",
                }
            },
            "tasks": [
                {
                    "type": "VERIFY_SHARE_CODE_TASK",
                    "id": "task-id-1",
                    "state": "DONE",
                    "created": "2026-02-05T11:33:46Z",
                    "last_updated": "2026-02-05T11:33:50Z",
                    "generated_media": [
                        {"id": "gen-media-1", "type": "PDF"},
                        {"id": "gen-media-2", "type": "IMAGE"},
                    ],
                }
            ],
        }

        result = ShareCodeResourceResponse(data)

        assert result.id == "abc12345-share-code-id"
        assert result.source == "END_USER"
        assert result.created_at == "2026-02-05T11:33:46Z"
        assert result.last_updated == "2026-02-05T11:33:50Z"
        assert result.lookup_profile.media.id == "lp-media-id"
        assert result.returned_profile.media.id == "rp-media-id"
        assert result.id_photo.media.id == "ip-media-id"
        assert result.file.media.id == "f-media-id"
        assert len(result.verify_share_code_tasks) == 1
        assert isinstance(
            result.verify_share_code_tasks[0], VerifyShareCodeTaskResponse
        )
        assert result.verify_share_code_tasks[0].id == "task-id-1"
        assert result.verify_share_code_tasks[0].state == "DONE"
        assert len(result.verify_share_code_tasks[0].generated_media) == 2


if __name__ == "__main__":
    unittest.main()
