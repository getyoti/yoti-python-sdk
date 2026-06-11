# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest

from yoti_python_sdk.doc_scan.session.retrieve.task_response import TaskResponse
from yoti_python_sdk.doc_scan.session.retrieve.verify_share_code_task_response import (
    VerifyShareCodeTaskResponse,
)


class VerifyShareCodeTaskResponseTest(unittest.TestCase):
    def test_should_be_instance_of_task_response(self):
        result = VerifyShareCodeTaskResponse({})

        assert isinstance(result, TaskResponse)

    def test_should_parse_task_fields(self):
        data = {
            "type": "VERIFY_SHARE_CODE_TASK",
            "id": "some-task-id",
            "state": "DONE",
            "created": "2026-02-05T11:33:46Z",
            "last_updated": "2026-02-05T11:33:50Z",
        }

        result = VerifyShareCodeTaskResponse(data)

        assert result.type == "VERIFY_SHARE_CODE_TASK"
        assert result.id == "some-task-id"
        assert result.state == "DONE"
        assert result.created is not None
        assert result.last_updated is not None

    def test_should_parse_generated_media(self):
        data = {
            "type": "VERIFY_SHARE_CODE_TASK",
            "id": "some-task-id",
            "state": "DONE",
            "generated_media": [
                {"id": "media-1", "type": "PDF"},
                {"id": "media-2", "type": "IMAGE"},
            ],
        }

        result = VerifyShareCodeTaskResponse(data)

        assert len(result.generated_media) == 2
        assert result.generated_media[0].id == "media-1"
        assert result.generated_media[0].type == "PDF"
        assert result.generated_media[1].id == "media-2"
        assert result.generated_media[1].type == "IMAGE"

    def test_should_parse_when_none(self):
        result = VerifyShareCodeTaskResponse(None)

        assert result.id is None
        assert result.type is None
        assert result.state is None


if __name__ == "__main__":
    unittest.main()
