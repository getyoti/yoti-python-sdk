from abc import ABCMeta
from abc import abstractmethod

from yoti_python_sdk.utils import YotiSerializable


class RequiredDocument(YotiSerializable):
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def type(self):
        raise NotImplementedError

    def __new__(cls, *args, **kwargs):
        if cls is RequiredDocument:
            raise TypeError("RequiredDocument may not be instantiated")
        return object.__new__(cls)
