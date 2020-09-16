from abc import ABCMeta
from abc import abstractmethod

from yoti_python_sdk.utils import YotiSerializable, remove_null_values


class RequestedTask(YotiSerializable):
    """
    Requests creation of a Task to be performed on each document
    """

    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def type(self):
        """
        Returns the type of the Task to create

        :return: the type
        :rtype: str
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def config(self):
        """
        Configuration to apply to the Task

        :return: the configuration
        """
        raise NotImplementedError

    def to_json(self):
        return remove_null_values({"type": self.type, "config": self.config})
