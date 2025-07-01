from abc import ABCMeta
from abc import abstractmethod

from yoti_python_sdk.utils import YotiSerializable


class SubRequestedCheck(YotiSerializable):
    """
    Requests creation of a SubCheck to be performed on a document
    """

    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def type(self):
        raise NotImplementedError

    def to_json(self):
        return remove_null_values({"type": self.type, "config": self.config})
