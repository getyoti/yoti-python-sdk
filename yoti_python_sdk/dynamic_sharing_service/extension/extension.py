# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class Extension(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    """
    @return A string label for the extension type
    """

    @property
    def extension_type(self):
        return self.__dict__.get("_Extension__extension_type", None)

    """
    @return The extension's data
    """

    @property
    def content(self):
        return self.__dict__.get("_Extension__content", None)

    @property
    def data(self):
        return {
            "type": self.extension_type,
            "content": self.content.data if self.content else {},
        }
