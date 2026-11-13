# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.utils import YotiSerializable, remove_null_values


class CompanyProfile(YotiSerializable):
    """
    Represents the company profile to be associated with an IDV session.
    """

    def __init__(self, company_name):
        """
        :param company_name: the name of the company
        :type company_name: str or None
        """
        self.__company_name = company_name

    @property
    def company_name(self):
        """
        The name of the company

        :return: the company name
        :rtype: str or None
        """
        return self.__company_name

    def to_json(self):
        return remove_null_values(
            {
                "company_name": self.company_name,
            }
        )
