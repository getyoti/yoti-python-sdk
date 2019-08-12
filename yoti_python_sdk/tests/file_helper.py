import binascii
import io
from os.path import abspath, dirname, join

FIXTURES_DIR = join(dirname(abspath(__file__)), "fixtures")


def get_file_bytes(file_path):
    base64_data = read_file(file_path)
    file_bytes = binascii.a2b_base64(base64_data)

    return file_bytes


def read_file(file_path):
    with io.open(file_path, mode="r", encoding="utf-8") as file:
        return file.read()
