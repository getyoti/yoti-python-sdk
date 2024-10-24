import base64
from google.protobuf.message import DecodeError
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from ..proto import EncryptedData_pb2

def decrypt_receipt_content(content, receipt_content_key):
    if not content:
        return None

    content_buffer = base64.b64decode(content)

    iv, cipher_text = decode_encrypted_data(content_buffer)

    cipher_text_buffer = base64.b64decode(cipher_text)
    iv_buffer = base64.b64decode(iv)

    return decrypt_aes_cbc(cipher_text_buffer, iv_buffer, receipt_content_key)

def decode_encrypted_data(binary_data):
    encrypted_data = EncryptedData_pb2.EncryptedData()

    try:
        encrypted_data.ParseFromString(binary_data)
    except DecodeError:
        raise ValueError("Failed to decode binary data")

    return (
        base64.b64encode(encrypted_data.iv).decode('utf-8'),
        base64.b64encode(encrypted_data.cipher_text).decode('utf-8'),
    )

def decrypt_aes_cbc(cipher_text, iv, secret):
    cipher = Cipher(algorithms.AES(secret), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(cipher_text) + decryptor.finalize()

    return strip_pkcs5_padding(decrypted_data)

def strip_pkcs5_padding(data):
    padding_length = data[-1]
    return data[:-padding_length]
