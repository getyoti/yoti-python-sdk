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
        return self.__name

    @property
    def value(self):
        return self.__value

    @property
    def anchors(self):
        return self.__anchors

    @property
    def sources(self):
        return list(
            filter(lambda a: a.anchor_type == config.ANCHOR_SOURCE, self.__anchors)
        )

    @property
    def verifiers(self):
        return list(
            filter(lambda a: a.anchor_type == config.ANCHOR_VERIFIER, self.__anchors)
        )

    @property
    def derivation(self):
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
        return SandboxAttributeBuilder()


class SandboxAttributeBuilder(object):
    def __init__(self):
        self.__name = None
        self.__value = None
        self.__anchors = None
        self.__derivation = None

    def with_name(self, name):
        self.__name = name
        return self

    def with_value(self, value):
        self.__value = value
        return self

    def with_anchors(self, anchors):
        self.__anchors = anchors
        return self

    def with_derivation(self, derivation):
        self.__derivation = derivation
        return self

    def build(self):
        return SandboxAttribute(
            self.__name, self.__value, self.__anchors, self.__derivation
        )
