# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.doc_scan import constants
from yoti_python_sdk.utils import YotiSerializable, remove_null_values
from .requested_check import RequestedCheck


class RequestedThirdPartyIdentityCheckConfig(YotiSerializable):
    """
    The configuration applied when creating a Third Party Identity Check
    """

    def to_json(self):
        return remove_null_values({})


class RequestedThirdPartyIdentityCheck(RequestedCheck):
    """
    Requests creation of a Third Party Identity check
    """

    def __init__(self, config):
        """
        :param config: the requested third party identity check configuration
        :type config: RequestedThirdPartyIdentityCheckConfig
        """
        self.__config = config

    @property
    def type(self):
        return constants.THIRD_PARTY_IDENTITY

    @property
    def config(self):
        return self.__config


class RequestedThirdPartyIdentityCheckBuilder:
    """
    Builder to assist creation of :class:`RequestedThirdPartyIdentityCheck`
    """

    def build(self=None):
        config = RequestedThirdPartyIdentityCheckConfig()
        return RequestedThirdPartyIdentityCheck(config)
