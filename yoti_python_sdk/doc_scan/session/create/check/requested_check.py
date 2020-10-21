from abc import ABCMeta
from abc import abstractmethod

from yoti_python_sdk.utils import YotiSerializable, remove_null_values


class RequestedCheck(YotiSerializable):
    """
    Requests creation of a Check to be performed on a document
    """

    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def type(self):
        """
        Return the type of the Check to create

        :return: the type
        :rtype: str
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def config(self):
        """
        Return configuration to apply to the Check

        :return: the configuration
        """
        raise NotImplementedError

    def to_json(self):
        return remove_null_values({"type": self.type, "config": self.config})
