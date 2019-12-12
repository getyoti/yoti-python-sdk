from yoti_python_sdk import config


class SandboxAttribute(object):
    def __init__(self, name=None, value=None, anchors=None, derivation=None):
        if name is None:
            name = ""

        if value is None:
            value = ""

        if anchors is None:
            anchors = []

        if derivation is None:
            derivation = ""

        self.__name = name
        self.__value = value
        self.__anchors = anchors
        self.__derivation = derivation

    @property
    def name(self):
        """
        Returns the name of the attribute

        :return: the name
        """
        return self.__name

    @property
    def value(self):
        """
        Returns the value of the attribute

        :return: the value
        """
        return self.__value

    @property
    def anchors(self):
        """
        Returns the anchors associated with the attribute

        :return: the anchors
        """
        return self.__anchors

    @property
    def sources(self):
        """
        Returns a filtered list of the associated anchors, only returning source anchors

        :return: list of filtered source anchors
        """
        return list(
            filter(lambda a: a.anchor_type == config.ANCHOR_SOURCE, self.__anchors)
        )

    @property
    def verifiers(self):
        """
        Returns a filtered list of the associated anchors, only returning verifier anchors

        :return: list of filtered verifier anchors
        """
        return list(
            filter(lambda a: a.anchor_type == config.ANCHOR_VERIFIER, self.__anchors)
        )

    @property
    def derivation(self):
        """
        Returns the derivation of the attribute

        :return: the derivation
        """
        return self.__derivation

    def __dict__(self):
        return {
            "name": self.name,
            "value": self.value,
            "anchors": self.anchors,
            "derivation": self.derivation,
        }

    @staticmethod
    def builder():
        """
        Creates an instance of the sandbox attribute builder

        :return: the sandbox attribute builder
        """
        return SandboxAttributeBuilder()


class SandboxAttributeBuilder(object):
    def __init__(self):
        self.__name = None
        self.__value = None
        self.__anchors = None
        self.__derivation = None

    def with_name(self, name):
        """
        Sets the name of the attribute on the builder

        :param str name: the name of the attribute
        :return: the updated builder
        """
        self.__name = name
        return self

    def with_value(self, value):
        """
        Sets the value of the attribute on the builder

        :param value: the value of the attribute
        :return: the updated builder
        """
        self.__value = value
        return self

    def with_anchors(self, anchors):
        """
        Sets the list of anchors associated with the attribute

        :param list[SandboxAnchor] anchors: the associated anchors
        :return:
        """
        self.__anchors = anchors
        return self

    def with_derivation(self, derivation):
        """
        Sets the derivation of the attribute on the builder

        :param str derivation: the derivation
        :return: the updated builder
        """
        self.__derivation = derivation
        return self

    def build(self):
        """
        Create an instance of SandboxAttribute using values supplied to the builder

        :return: instance of SandboxAttribute
        """
        return SandboxAttribute(
            self.__name, self.__value, self.__anchors, self.__derivation
        )
