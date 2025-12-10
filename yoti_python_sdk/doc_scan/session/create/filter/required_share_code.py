# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.utils import YotiSerializable, remove_null_values


class RequiredShareCode(YotiSerializable):
    """
    Represents a required share code for session creation
    """

    def __init__(self, issuer=None, scheme=None):
        """
        :param issuer: the issuer of the share code
        :type issuer: str or None
        :param scheme: the scheme of the share code
        :type scheme: str or None
        """
        self.__issuer = issuer
        self.__scheme = scheme

    @property
    def issuer(self):
        """
        The issuer of the share code

        :return: the issuer
        :rtype: str or None
        """
        return self.__issuer

    @property
    def scheme(self):
        """
        The scheme of the share code

        :return: the scheme
        :rtype: str or None
        """
        return self.__scheme

    def to_json(self):
        return remove_null_values({
            "issuer": self.issuer,
            "scheme": self.scheme,
        })


class RequiredShareCodeBuilder(object):
    """
    Builder used to assist the creation of a required share code.

    Example::

        required_share_code = (RequiredShareCodeBuilder()
                               .with_issuer("some-issuer")
                               .with_scheme("some-scheme")
                               .build())

    """

    def __init__(self):
        self.__issuer = None
        self.__scheme = None

    def with_issuer(self, issuer):
        """
        Sets the issuer of the required share code

        :param issuer: the issuer
        :type issuer: str
        :return: the builder
        :rtype: RequiredShareCodeBuilder
        """
        self.__issuer = issuer
        return self

    def with_scheme(self, scheme):
        """
        Sets the scheme of the required share code

        :param scheme: the scheme
        :type scheme: str
        :return: the builder
        :rtype: RequiredShareCodeBuilder
        """
        self.__scheme = scheme
        return self

    def build(self):
        """
        Builds a required share code, using the values supplied to the builder

        :return: the required share code
        :rtype: RequiredShareCode
        """
        return RequiredShareCode(self.__issuer, self.__scheme)
