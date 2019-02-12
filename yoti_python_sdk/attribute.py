from yoti_python_sdk import config


class Attribute:
    def __init__(self, name="", value="", anchors=None):
        if anchors is None:
            anchors = {}
        self.__name = name
        self.__value = value
        self.__anchors = anchors

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
        return list(filter(lambda a: a.anchor_type == config.ANCHOR_SOURCE, self.__anchors))

    @property
    def verifiers(self):
        return list(filter(lambda a: a.anchor_type == config.ANCHOR_VERIFIER, self.__anchors))
