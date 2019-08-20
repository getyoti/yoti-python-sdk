from yoti_python_sdk import config


class SandboxAnchor(object):
    def __init__(self, anchor_type=None, sub_type=None, value=None, timestamp=None):
        if anchor_type is None:
            anchor_type = config.UNKNOWN_ANCHOR_TYPE
        if sub_type is None:
            sub_type = ""
        if value is None:
            value = ""

        self.__anchor_type = anchor_type
        self.__sub_type = sub_type
        self.__value = value
        self.__timestamp = timestamp

    @property
    def anchor_type(self):
        return self.__anchor_type

    @property
    def sub_type(self):
        return self.__sub_type

    @property
    def value(self):
        return self.__value

    @property
    def timestamp(self):
        return self.__timestamp

    @staticmethod
    def builder(self):
        return SandboxAnchorBuilder()


class SandboxAnchorBuilder(object):
    def __init__(self):
        self.__type = None
        self.__value = None
        self.__sub_type = None
        self.__timestamp = None

    def with_type(self, type):
        self.__type = type
        return self

    def with_value(self, value):
        self.__value = value
        return self

    def with_sub_type(self, sub_type):
        self.__sub_type = sub_type
        return self

    def with_timestamp(self, timestamp):
        self.__timestamp = timestamp
        return self

    def build(self):
        return SandboxAnchor(
            self.__type, self.__sub_type, self.__value, self.__timestamp
        )
