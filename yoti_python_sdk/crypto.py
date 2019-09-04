# -*- coding: utf-8 -*-
from cryptography.fernet import hashes, base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from os.path import isfile, expanduser
from past.builtins import basestring


class Crypto:
    def __init__(self, pem_container):
        self.private_key = serialization.load_pem_private_key(
            data=pem_container, password=None, backend=default_backend()
        )

    def get_public_key(self):
        public_key = self.private_key.public_key()
        der = public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return base64.b64encode(der).decode("utf-8")

    def decrypt_token(self, encrypted_token):
        try:
            if not isinstance(encrypted_token, bytes):
                # On Python 2 the token is str and to b64decode it we need bytes or unicode
                encrypted_token = encrypted_token.encode("utf-8")

            data = base64.urlsafe_b64decode(encrypted_token)
            decrypted = self.private_key.decrypt(
                ciphertext=data, padding=padding.PKCS1v15()
            )
            return decrypted

        except Exception as exc:
            raise ValueError(
                "Could not decrypt token: {0}, {1}".format(encrypted_token, exc)
            )

    def sign(self, message):
        signature = self.private_key.sign(
            data=message.encode("utf-8"),
            padding=padding.PKCS1v15(),
            algorithm=hashes.SHA256(),
        )
        return base64.b64encode(signature).decode("utf-8")

    @staticmethod
    def decipher(key, iv, cipher_text):
        decryptor = Cipher(
            algorithm=algorithms.AES(key), mode=modes.CBC(iv), backend=default_backend()
        ).decryptor()
        plaintext = decryptor.update(cipher_text) + decryptor.finalize()

        return Crypto.strip_pkcs5_padding(plaintext)

    @staticmethod
    def strip_pkcs5_padding(data):
        if isinstance(data, str):
            data = bytearray(data)

        number_of_padded_bytes = data[-1]
        stripped = data[:-number_of_padded_bytes]

        if isinstance(stripped, bytearray):
            stripped = str(stripped)
        return stripped

    @staticmethod
    def read_pem_file(key_file_path, error_source=None):
        try:
            key_file_path = expanduser(key_file_path)

            if not isinstance(key_file_path, basestring) or not isfile(key_file_path):
                raise IOError("File not found: {0}".format(key_file_path))

            with open(key_file_path, "rb") as pem_file:
                return Crypto(pem_file.read().strip())
        except (AttributeError, IOError, TypeError, OSError) as exc:
            error = "Could not read private key file: '{0}', passed as: {1}".format(
                key_file_path, error_source
            )
            exception = "{0}: {1}".format(type(exc).__name__, exc)
            raise RuntimeError("{0}: {1}".format(error, exception))
