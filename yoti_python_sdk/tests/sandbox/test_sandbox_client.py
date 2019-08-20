from yoti_python_sdk.sandbox.client import SandboxClient

import pytest


def test_builder_should_throw_exception_for_missing_sdk_id():
    builder = SandboxClient.builder()
    with pytest.raises(ValueError):
        builder.build()
