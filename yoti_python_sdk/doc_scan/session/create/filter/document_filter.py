from abc import ABCMeta

from yoti_python_sdk.utils import YotiSerializable, remove_null_values


class DocumentFilter(YotiSerializable):
    __metaclass__ = ABCMeta

    def __init__(self, filter_type):
        self.__filter_type = filter_type

    @property
    def type(self):
        return self.__filter_type

    def to_json(self):
        return remove_null_values({"type": self.type})
