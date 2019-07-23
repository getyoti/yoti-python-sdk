# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class ExtensionBuilder(object):
    def __init__(self):
        self.__extension = {}

    """
    @param extension_type String label for the extension type
    """

    def with_extension_type(self, extension_type):
        self.__extension["type"] = extension_type
        return self

    """
    @param content The extension content
    """

    def with_content(self, content):
        self.__extension["content"] = content
        return self

    """
    @return Dictionary representation of an extension
    """

    def build(self):
        return self.__extension.copy()
