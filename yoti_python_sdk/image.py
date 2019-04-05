# -*- coding: utf-8 -*-
from cryptography.fernet import base64

from yoti_python_sdk.protobuf.protobuf import Protobuf


class Image:
    def __init__(self, image_bytes, image_content_type):
        if image_content_type in Image.allowed_types():
            self.__data = image_bytes
            self.__content_type = image_content_type
        else:
            raise TypeError("Content type '{0}' is not a supported image type".format(image_content_type))

    @staticmethod
    def allowed_types():
        return [Protobuf.CT_PNG, Protobuf.CT_JPEG]

    @property
    def data(self):
        return self.__data

    @property
    def content_type(self):
        return self.__content_type

    def mime_type(self):
        if self.__content_type == Protobuf.CT_JPEG:
            return "image/jpeg"
        elif self.__content_type == Protobuf.CT_PNG:
            return "image/png"
        else:
            return ""

    def base64_content(self):
        if self.__content_type == Protobuf.CT_JPEG:
            data = base64.b64encode(self.__data).decode('utf-8')
            return 'data:image/jpeg;base64,{0}'.format(data)
        elif self.__content_type == Protobuf.CT_PNG:
            data = base64.b64encode(self.__data).decode('utf-8')
            return 'data:image/png;base64,{0}'.format(data)

        raise TypeError("Content type '{0}' is not a supported image type".format(self.__content_type))
