import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from yoti_python_sdk.protobuf import protobuf
from yoti_python_sdk.profile import Profile
from ..user_content import UserContent
from .utils import decrypt_receipt_content


def unwrap_receipt_key(wrapped_receipt_key, encrypted_item_key, item_key_iv, pem):
    # Decode the base64 encoded inputs
    wrapped_receipt_key_buffer = base64.b64decode(wrapped_receipt_key)
    encrypted_item_key_buffer = base64.b64decode(encrypted_item_key)
    item_key_iv_buffer = base64.b64decode(item_key_iv)

    # Load the private key from PEM file
    private_key = load_private_key(pem)

    # Decrypt the item key
    decrypted_item_key = decrypt_item_key(private_key, encrypted_item_key_buffer)

    # Decrypt the wrapped receipt key
    return decrypt_wrapped_receipt_key(decrypted_item_key, wrapped_receipt_key_buffer, item_key_iv_buffer)


def load_private_key(pem):
    with open(pem, "rb") as key_file:
        return serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )


def decrypt_item_key(private_key, encrypted_item_key_buffer):
    return private_key.decrypt(
        encrypted_item_key_buffer,
        padding.PKCS1v15()
    )


def decrypt_wrapped_receipt_key(decrypted_item_key, wrapped_receipt_key_buffer, item_key_iv_buffer):
    tag_size = 16  # Size of the authentication tag

    # Separate the authentication tag from the ciphertext
    cipher_text, tag = wrapped_receipt_key_buffer[:-tag_size], wrapped_receipt_key_buffer[-tag_size:]

    # Create the cipher and decrypt the data
    cipher = Cipher(algorithms.AES(decrypted_item_key), modes.GCM(item_key_iv_buffer, tag), backend=default_backend())
    decryptor = cipher.decryptor()

    return decryptor.update(cipher_text) + decryptor.finalize()


def build_user_content_from_encrypted_content(content, receipt_content_key):
    if content is None:
        content = {'profile': '', 'extraData': ''}

    attributes, extra_data = decrypt_and_extract_content_data(content, receipt_content_key)
    return UserContent(attributes, extra_data)


def decrypt_and_extract_content_data(content=None, receipt_content_key=None):
    if content is None:
        content = {'profile': '', 'extraData': ''}

    decrypted_profile = decrypt_receipt_content(content.get('profile'), receipt_content_key)
    decrypted_extra_data = decrypt_receipt_content(content.get('extraData'), receipt_content_key)

    attributes = extract_attributes(decrypted_profile)
    extracted_extra_data = decrypted_extra_data if decrypted_extra_data else None

    return attributes, extracted_extra_data


def extract_attributes(decrypted_profile):
    proto = protobuf.Protobuf()

    if decrypted_profile:
        user_profile_attribute_list = proto.attribute_list(decrypted_profile)
        return user_profile_attribute_list.attributes if hasattr(user_profile_attribute_list, 'attributes') else None

    return None
