# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class WantedAttributeBuilder(object):
    """
    Builder for WantedAttribute
    """

    def __init__(self):
        self.__attribute = {}
        self.__constraints = []

    def with_name(self, name):
        """
        :param name: Sets name
        """
        self.__attribute["name"] = name
        return self

    def with_derivation(self, derivation):
        """
        :param derivation: Sets derivation
        """
        self.__attribute["derivation"] = derivation
        return self

    def with_accept_self_asserted(self, value=True):
        """
        :param value: True if self-asserted details are allowed
        """
        self.__attribute["accept_self_asserted"] = value
        return self

    def with_constraint(self, constraint):
        """
        :param constraint: Adds a constraint (e.g. a source constraint) to the
                            wanted attribute
        """
        if isinstance(constraint, list):
            self.__constraints.extend(constraint)
        else:
            self.__constraints.append(constraint)
        return self

    def build(self):
        """
        :return: The wanted attribute object
        """
        if self.__attribute.get("name", None) is None or self.__attribute["name"] == "":
            raise ValueError
        attribute = self.__attribute.copy()
        attribute["constraints"] = self.__constraints[:]
        return attribute
