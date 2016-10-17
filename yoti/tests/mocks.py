from uuid import UUID


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, status_code, text):
            self.status_code = status_code
            self.text = text

    with open('yoti/tests/fixtures/response.txt', 'r') as f:
        response = f.read()
    return MockResponse(status_code=200, text=response)


def mocked_timestamp():
    return 1476441361.2395663


def mocked_uuid4():
    return UUID('35351ced-96a4-4fc8-994e-98f98045ff7e')
