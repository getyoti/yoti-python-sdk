# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.profile import Profile

from .base_content import BaseContent

class UserContent(BaseContent):

    def __init__(self, attributes=None, extra_data=None):
        """
        :param data: the attributes
        :type data: array or None
        :param extra_data: the extra data
        :type extra_data: dict or None
        """
        super().__init__(extra_data)
        if attributes is None:
            attributes = []

        self.__profile = Profile(attributes)

    def to_dict(self):
        return {
            'profile': self.__profile,
        }

    @property
    def profile(self):
        """
        :return: the profile
        :rtype: Profile
        """
        return self.__profile
   