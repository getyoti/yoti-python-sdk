from yoti_python_sdk import config


class Attribute:
    def __init__(self, name=None, value=None, anchors=None, icon = None):
        if name is None:
            name = ""
        if value is None:
            value = ""
        if anchors is None:
            anchors = {}
        self.__name = name
        self.__value = value
        self.__anchors = anchors
        self.__icon = icon

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
    def icon(self):
        return self.__icon
