from yoti_python_sdk import config


class attribute:
    name = ""
    value = ""
    anchors = {}

    def __init__(self, name, value, anchors):
        self.name = name
        self.value = value
        self.anchors = anchors

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def get_anchors(self):
        return self.anchors

    def get_sources(self):
        return list(filter(lambda a: a.anchor_type == config.ANCHOR_SOURCE, self.anchors))

    def get_verifiers(self):
        return list(filter(lambda a: a.anchor_type == config.ANCHOR_VERIFIER, self.anchors))
