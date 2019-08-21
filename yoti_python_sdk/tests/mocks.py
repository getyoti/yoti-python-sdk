from uuid import UUID


class MockResponse:
    def __init__(self, status_code, text):
        self.status_code = status_code
        self.text = text


def mocked_requests_get(*args, **kwargs):
    with open("yoti_python_sdk/tests/fixtures/response.txt", "r") as f:
        response = f.read()
    return MockResponse(status_code=200, text=response)


def mocked_requests_post_aml_profile(*args, **kwargs):
    with open("yoti_python_sdk/tests/fixtures/aml_response.txt", "r") as f:
        response = f.read()
    return MockResponse(status_code=200, text=response)


def mocked_requests_post_aml_profile_not_found(*args, **kwargs):
    return MockResponse(status_code=404, text="Not Found")


def mocked_requests_get_null_profile(*args, **kwargs):
    with open("yoti_python_sdk/tests/fixtures/response_null_profile.txt", "r") as f:
        response = f.read()
    return MockResponse(status_code=200, text=response)


def mocked_requests_get_empty_profile(*args, **kwargs):
    with open("yoti_python_sdk/tests/fixtures/response_empty_profile.txt", "r") as f:
        response = f.read()
    return MockResponse(status_code=200, text=response)


def mocked_requests_get_missing_profile(*args, **kwargs):
    with open("yoti_python_sdk/tests/fixtures/response_missing_profile.txt", "r") as f:
        response = f.read()
    return MockResponse(status_code=200, text=response)


def mocked_timestamp():
    return 1476441361.2395663


def mocked_uuid4():
    return UUID("35351ced-96a4-4fc8-994e-98f98045ff7e")


def mocked_requests_post_share_url(*args, **kwargs):
    with open("yoti_python_sdk/tests/fixtures/response_share_url.txt", "r") as f:
        response = f.read()
    return MockResponse(status_code=200, text=response)


def mocked_requests_post_share_url_invalid_json(*args, **kwargs):
    return MockResponse(status_code=400, text="Invalid json")


def mocked_requests_post_share_url_app_not_found(*args, **kwargs):
    return MockResponse(status_code=404, text="Application not found")
