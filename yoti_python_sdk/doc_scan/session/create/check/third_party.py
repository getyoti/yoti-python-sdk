from yoti_python_sdk.doc_scan import constants
from yoti_python_sdk.utils import (
    YotiSerializable,
    remove_null_values,
)
from .requested_check import RequestedCheck


class RequestedThirdPartyCheckConfig(YotiSerializable):
    """
    The configuration applied when creating a ThirdPartyCheck
    """

    def __init__(self, manual_check):
        """
        :param manual_check: should be checked manually
        :type manual_check: str
        """

        self.__manual_check = manual_check

    @property
    def manual_check(self):
        """
        The manual_check attribute

        :return: manual_check string value
        """
        return self.__manual_check

    def to_json(self):
        return remove_null_values({"manual_check": self.manual_check})


class RequestedThirdPartyCheck(RequestedCheck):
    """
    Requests creation of a Third Party Check.

    Check is performed on user, not document.
    At least one document is needed for extracting the data used in this check.
    If no documents are provided, the Supplementary Document is optional.
    """

    def __init__(self, config):
        """
        :param config: the requested THIRD PARTY CHECK configuration
        :type config: ThirdPartyCheckConfig
        """
        self.__config = config

    @property
    def type(self):
        """
        The type of the THIRD PARTY CHECK

        return: the THIRD PARTY CHECK

        """
        return constants.THIRD_PARTY_IDENTITY

    @property
    def config(self):
        return self.__config


class RequestedThirdPartyCheckBuilder(object):
    """
    Builder to assist creation of :class:`ThirdPartyCheck`
    """

    def __init__(self):
        self.__manual_check = None

    def with_manual_check(self, manual_check):
        """
        Sets the manual_check attrbiute

        :param manual_check: value for manual_check
        :type max_retries: str
        :return: the builder
        :rtype: RequestedThirdPartyCheckBuilder
        """
        self.__manual_check = manual_check
        return self

    def build(self):
        return RequestedThirdPartyCheck(
            config=RequestedThirdPartyCheckConfig(manual_check=self.__manual_check or 'NEVER')
        )
