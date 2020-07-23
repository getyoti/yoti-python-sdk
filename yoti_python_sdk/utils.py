import base64
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


def urlsafe_b64encode_unpadded(b):
    """
    Base64 URL encode without padding
    \
    :param b: the bytes to encode
    :type b: bytes
    :return: the encoded string
    :rtype: string
    """
    return base64.urlsafe_b64encode(b).decode("utf-8").rstrip("=")


def urlsafe_b64decode_unpadded(s):
    """
    Base64 URL decode without padding
    \
    :param s: the string to decode
    :type s: string
    :return: the decoded bytes
    :rtype: bytes
    """
    return base64.urlsafe_b64decode((s + "==").encode("utf-8"))
