# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class TransactionalFlowExtensionBuilder(object):
    TRANSACTIONAL_FLOW = "TRANSACTIONAL_FLOW"

    def __init__(self):
        self.__extension = {}
        self.__extension["type"] = self.TRANSACTIONAL_FLOW

    def with_content(self, content):
        """
        @param content The extension content
        """
        self.__extension["content"] = content
        return self

    def build(self):
        """
        @return Dictionary representation of an extension
        """
        return self.__extension.copy()
