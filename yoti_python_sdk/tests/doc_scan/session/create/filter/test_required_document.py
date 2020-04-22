import pytest

from yoti_python_sdk.doc_scan.session.create.filter.required_document import (
    RequiredDocument,
)


def test_should_not_allow_direct_instantiation():
    with pytest.raises(TypeError) as e:
        RequiredDocument()

    assert str(e.value) == "RequiredDocument may not be instantiated"
