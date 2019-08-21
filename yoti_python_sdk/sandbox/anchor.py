from yoti_python_sdk.anchor import UNKNOWN_ANCHOR_TYPE


class SandboxAnchor(object):
    def __init__(self, anchor_type=None, sub_type=None, value=None, timestamp=None):
        if anchor_type is None:
            anchor_type = UNKNOWN_ANCHOR_TYPE
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
        """
        Returns the anchor type

        :return: the type
        """
        return self.__anchor_type

    @property
    def sub_type(self):
        """
        Returns the anchor sub-type

        :return: the sub-type
        """
        return self.__sub_type

    @property
    def value(self):
        """
        Returns the anchor value

        :return: the value
        """
        return self.__value

    @property
    def timestamp(self):
        """
        Returns the anchor timestamp

        :return: the timestamp
        """
        return self.__timestamp

    def __dict__(self):
        return {
            "type": self.anchor_type,
            "value": self.value,
            "sub_type": self.sub_type,
            "timestamp": self.timestamp,
        }

    @staticmethod
    def builder():
        """
        Creates an instance of the sandbox anchor builder

        :return: instance of SandboxAnchorBuilder
        """
        return SandboxAnchorBuilder()


class SandboxAnchorBuilder(object):
    def __init__(self):
        self.__type = None
        self.__value = None
        self.__sub_type = None
        self.__timestamp = None

    def with_type(self, type):
        """
        Sets the type of the anchor on the builder

        :param str type: the anchor type
        :return: the updated builder
        """
        self.__type = type
        return self

    def with_value(self, value):
        """
        Sets the value of the anchor on the builder

        :param str value: the anchor value
        :return: the updated builder
        """
        self.__value = value
        return self

    def with_sub_type(self, sub_type):
        """
        Sets the sub type of the anchor on the builder

        :param str sub_type: the anchor sub type
        :return: the updated builder
        """
        self.__sub_type = sub_type
        return self

    def with_timestamp(self, timestamp):
        """
        Sets the timestamp of the anchor on the builder

        :param int timestamp: the anchor timestamp
        :return: the updated builder
        """
        self.__timestamp = timestamp
        return self

    def build(self):
        """
        Creates a SandboxAnchor using values supplied to the builder

        :return: the sandbox anchor
        """
        return SandboxAnchor(
            self.__type, self.__sub_type, self.__value, self.__timestamp
        )
