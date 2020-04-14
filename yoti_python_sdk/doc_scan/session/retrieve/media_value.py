# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64


class MediaValue(object):
    def __init__(self, content_type, content):
        self.__mime_type = content_type
        self.__content = content

    @property
    def mime_type(self):
        return self.__mime_type

    @property
    def content(self):
        return self.__content

    @property
    def base64_content(self):
        return "data:%s;base64,%s" % (
            self.mime_type,
            base64.b64encode(self.__content).decode("utf-8"),
        )
