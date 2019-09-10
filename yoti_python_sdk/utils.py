import uuid
import time


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
