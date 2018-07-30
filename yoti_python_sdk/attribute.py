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
