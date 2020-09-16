import time
import uuid
from abc import ABCMeta
from abc import abstractmethod
from json import JSONEncoder


class YotiSerializable(object):
    """
    Used to describe a class that is serializable by :class:`YotiEncoder`.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def to_json(self):
        raise NotImplementedError


class YotiEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, YotiSerializable):
            return o.to_json()
        return JSONEncoder.default(self, o)


def create_nonce():
    """
    Create and return a nonce
    \
    :return: the nonce
    """
    return uuid.uuid4()


def create_timestamp():
    """
    Create and return a timestamp

    :return: the timestamp as a int
    """
    return int(time.time() * 1000)


def remove_null_values(d):
    """
    Delete keys with the value ``None`` in a dictionary, recursively. (None serializes to null)
    """
    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            remove_null_values(value)
    return d
