import unittest

from yoti_python_sdk.doc_scan.session.retrieve.face_capture_response import FaceCaptureResponse
from yoti_python_sdk.doc_scan.session.retrieve.media_response import MediaResponse


def test_should_not_throw_exception_if_data_is_none():
    result = FaceCaptureResponse()

    assert result.id is None
    assert len(result.tasks) == 0
    assert isinstance(result.image, MediaResponse)


def test_should_parse_id():
    test_data = {
        "id": 123
    }
    result = FaceCaptureResponse(data=test_data)

    assert result.id == test_data['id']


def test_should_parse_source():
    test_data = {
        "source": "SomeSource"
    }
    result = FaceCaptureResponse(data=test_data)

    assert result.source == test_data['source']


def test_should_parse_image_to_image_instance():
    test_data = {
        "image": {}
    }
    result = FaceCaptureResponse(data=test_data)

    assert isinstance(result.image, MediaResponse)

    test_data = {
        "image": {
            "id": 123,
            "type": "DummyType",
        }
    }
    result = FaceCaptureResponse(data=test_data)
    assert isinstance(result.image, MediaResponse)
    assert result.image.id == test_data["image"]["id"]
    assert result.image.type == test_data["image"]["type"]


if __name__ == "__main__":
    unittest.main()
