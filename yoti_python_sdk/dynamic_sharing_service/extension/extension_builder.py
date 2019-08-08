# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class ExtensionBuilder(object):
    def __init__(self):
        self.__extension = {}

    def with_extension_type(self, extension_type):
        """
        @param extension_type String label for the extension type
        """
        self.__extension["type"] = extension_type
        return self

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
