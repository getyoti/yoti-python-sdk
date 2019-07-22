# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .extension import Extension


class ExtensionBuilder(object):
    def __init__(self):
        self.__extension = {}

    """
    @param extension_type String label for the extension type
    """

    def with_extension_type(self, extension_type):
        self.__extension["_Extension__extension_type"] = extension_type
        return self

    """
    @param content The extension content
    """

    def with_content(self, content):
        self.__extension["_Extension__content"] = content
        return self

    """
    @return An Extension object
    """

    def build(self):
        return Extension(**self.__extension)
