# -*- coding: utf-8 -*-
from cryptography.fernet import hashes, base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)


class Crypto:
    def __init__(self, pem_container):
        self.private_key = serialization.load_pem_private_key(
            data=pem_container,
            password=None,
            backend=default_backend()
        )

    def get_public_key(self):
        public_key = self.private_key.public_key()
        der = public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return base64.b64encode(der).decode('utf-8')

    def decrypt_token(self, encrypted_token):
        try:
            if not isinstance(encrypted_token, bytes):
                # On Python 2 the token is str and to b64decode it we need bytes or unicode
                encrypted_token = encrypted_token.encode('utf-8')

            data = base64.urlsafe_b64decode(encrypted_token)
            decrypted = self.private_key.decrypt(
                ciphertext=data,
                padding=padding.PKCS1v15()
            )
            return decrypted

        except Exception as exc:
            raise ValueError(
                'Could not decrypt token: {0}, {1}'.format(
                    encrypted_token, exc
                )
            )

    def sign(self, message):
        signature = self.private_key.sign(
            data=message.encode('utf-8'),
            padding=padding.PKCS1v15(),
            algorithm=hashes.SHA256()
        )
        return base64.b64encode(signature).decode('utf-8')

    @staticmethod
    def decipher(key, iv, cipher_text):
        decryptor = Cipher(
            algorithm=algorithms.AES(key),
            mode=modes.CBC(iv),
            backend=default_backend()
        ).decryptor()
        return decryptor.update(cipher_text) + decryptor.finalize()
