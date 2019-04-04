from yoti_python_sdk.protobuf.protobuf import Protobuf


class Image:
    def __init__(self, image_bytes, image_content_type):
        if image_content_type == Protobuf.CT_JPEG or image_content_type == Protobuf.CT_PNG:
            self.__data = image_bytes
            self.__content_type = image_content_type
        else:
            raise TypeError("Content type '{0}' is not a supported image type".format(image_content_type))

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
        return Protobuf().image_uri_based_on_content_type(
            # TODO: move image_uri_based_on_content_type method to this class
            self.__data,
            self.__content_type)
