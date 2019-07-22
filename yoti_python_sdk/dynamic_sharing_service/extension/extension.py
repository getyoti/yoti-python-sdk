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
        return self.__extension_type

    """
    @return The extension's data
    """

    @property
    def content(self):
        return self.__content
