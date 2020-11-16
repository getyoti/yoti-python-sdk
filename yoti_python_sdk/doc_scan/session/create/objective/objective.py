from abc import ABCMeta
from abc import abstractmethod

from yoti_python_sdk.utils import YotiSerializable, remove_null_values


class Objective(YotiSerializable):
    """
    The objective of the document
    """

    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def type(self):
        """
        Return the type of the objective

        :return: the type
        :rtype: str
        """
        raise NotImplementedError

    def to_json(self):
        return remove_null_values({"type": self.type})
