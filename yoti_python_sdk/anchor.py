from yoti_python_sdk import config

UNKNOWN_EXTENSION = ""
SOURCE_EXTENSION = "1.3.6.1.4.1.47127.1.1.1"
VERIFIER_EXTENSION = "1.3.6.1.4.1.47127.1.1.2"

UNKNOWN_ANCHOR_VALUE = ""


class Anchor:
    def __init__(
        self,
        anchor_type=None,
        sub_type=None,
        value=None,
        signed_timestamp=None,
        origin_server_certs=None,
    ):
        if sub_type is None:
            sub_type = ""

        if value is None:
            value = ""

        if anchor_type is None:
            anchor_type = config.ANCHOR_UNKNOWN

        self.__anchor_type = anchor_type
        self.__sub_type = sub_type
        self.__value = value
        self.__signed_timestamp = signed_timestamp
        self.__origin_server_certs = origin_server_certs

    def __iter__(self):
        return self

    def __next__(self):
        self.idx += 1
        try:
            return self.data[self.idx - 1]
        except IndexError:
            self.idx = 0
            raise StopIteration

    @property
    def anchor_type(self):
        return self.__anchor_type

    @property
    def value(self):
        return self.__value

    @property
    def sub_type(self):
        return self.__sub_type

    @property
    def signed_timestamp(self):
        return self.__signed_timestamp

    @property
    def origin_server_certs(self):
        return self.__origin_server_certs
