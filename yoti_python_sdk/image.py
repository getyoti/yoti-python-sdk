# -*- coding: utf-8 -*-
from cryptography.fernet import base64

from yoti_python_sdk.protobuf.protobuf import Protobuf

CONTENT_TYPE_JPEG = "jpeg"
CONTENT_TYPE_PNG = "png"


class Image:
    def __init__(self, image_bytes, image_content_type):
        if image_content_type == Protobuf.CT_JPEG:
            self.__content_type = CONTENT_TYPE_JPEG
        elif image_content_type == Protobuf.CT_PNG:
            self.__content_type = CONTENT_TYPE_PNG
        else:
            raise TypeError(
                "Content type '{0}' is not a supported image type".format(
                    image_content_type
                )
            )

        self.__data = image_bytes

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
        return "image/{0}".format(self.__content_type)

    def base64_content(self):
        data = base64.b64encode(self.__data).decode("utf-8")
        return "data:{0};base64,{1}".format(self.mime_type(), data)
