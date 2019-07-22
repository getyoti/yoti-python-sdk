# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .extension_builder import ExtensionBuilder


class TransactionalFlowExtensionBuilder(ExtensionBuilder):
    TRANSACTIONAL_FLOW = "TRANSACTIONAL_FLOW"

    def __init__(self):
        super().__init__()
        self.with_extension_type(self.TRANSACTIONAL_FLOW)
