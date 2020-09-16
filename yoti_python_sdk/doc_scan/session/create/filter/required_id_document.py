from yoti_python_sdk.doc_scan.constants import ID_DOCUMENT
from yoti_python_sdk.utils import remove_null_values
from .document_filter import DocumentFilter  # noqa: F401
from .required_document import RequiredDocument


class RequiredIdDocument(RequiredDocument):
    def __init__(self, doc_filter=None):
        """
        :param doc_filter: the filter for the document
        :type doc_filter:
        """
        self.__doc_filter = doc_filter

    @property
    def type(self):
        return ID_DOCUMENT

    @property
    def filter(self):
        return self.__doc_filter

    def to_json(self):
        return remove_null_values({"type": self.type, "filter": self.__doc_filter})


class RequiredIdDocumentBuilder(object):
    """
    Builder used to assist the creation of a required identity document.

    Example::

        required_id_document = (RequiredIdDocumentBuilder()
                                .with_filter(some_filter)
                                .build())

    """

    def __init__(self):
        self.__id_document_filter = None

    def with_filter(self, id_document_filter):
        """
        Sets the filter on the required ID document

        :param id_document_filter: the filter
        :type id_document_filter: DocumentFilter
        :return: the builder
        :rtype: RequiredIdDocumentBuilder
        """
        self.__id_document_filter = id_document_filter
        return self

    def build(self):
        """
        Builds a required ID document, using the values supplied to the builder

        :return: the required ID document
        :rtype: RequiredIdDocument
        """
        return RequiredIdDocument(self.__id_document_filter)
