class SupportedDocument(object):
    def __init__(self, data=None):
        if data is None:
            data = dict()

        self.__type = data.get("type", None)
        self.__is_strictly_latin = data.get("is_strictly_latin", None)

    @property
    def type(self):
        return self.__type

    @property
    def is_strictly_latin(self):
        return self.__is_strictly_latin


class SupportedCountry(object):
    def __init__(self, data=None):
        if data is None:
            data = dict()

        self.__code = data.get("code", None)
        self.__supported_documents = [
            SupportedDocument(document)
            for document in data.get("supported_documents", [])
        ]

    @property
    def code(self):
        return self.__code

    @property
    def supported_documents(self):
        return self.__supported_documents


class SupportedDocumentsResponse(object):
    def __init__(self, data=None):
        if data is None:
            data = dict()

        self.__supported_countries = [
            SupportedCountry(country) for country in data.get("supported_countries", [])
        ]

    @property
    def supported_countries(self):
        return self.__supported_countries
