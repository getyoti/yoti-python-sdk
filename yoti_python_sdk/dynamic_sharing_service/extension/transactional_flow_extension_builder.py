# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class TransactionalFlowExtensionBuilder(object):
    TRANSACTIONAL_FLOW = "TRANSACTIONAL_FLOW"

    def __init__(self):
        super(TransactionalFlowExtensionBuilder, self).__init__()
        self.with_extension_type(self.TRANSACTIONAL_FLOW)

    def with_content(self, content):
        """
        @param content The extension content
        """
        self.__extension["content"] = content

    def build(self):
        """
        @return Dictionary representation of an extension
        """
        return self.__extension.copy()
