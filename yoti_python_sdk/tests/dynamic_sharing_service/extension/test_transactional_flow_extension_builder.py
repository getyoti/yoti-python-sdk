# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.dynamic_sharing_service.extension.transactional_flow_extension_builder import (
    TransactionalFlowExtensionBuilder,
)


def test_should_build():
    TRANSACTIONAL_FLOW = "TRANSACTIONAL_FLOW"
    EXTENSION_CONTENT = 99

    extension = (
        TransactionalFlowExtensionBuilder().with_content(EXTENSION_CONTENT).build()
    )

    assert extension["type"] == TRANSACTIONAL_FLOW
    assert extension["content"] == EXTENSION_CONTENT
