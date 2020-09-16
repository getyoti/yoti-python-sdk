from yoti_python_sdk.doc_scan.constants import (
    DOCUMENT_RESTRICTIONS,
    INCLUSION_BLACKLIST,
    INCLUSION_WHITELIST,
)
from yoti_python_sdk.utils import YotiSerializable, remove_null_values
from .document_filter import DocumentFilter


class DocumentRestriction(YotiSerializable):
    def __init__(self, country_codes, document_types):
        self.__country_codes = country_codes
        self.__document_types = document_types

    @property
    def country_codes(self):
        return self.__country_codes

    @property
    def document_types(self):
        return self.__document_types

    def to_json(self):
        return remove_null_values(
            {
                "country_codes": self.country_codes,
                "document_types": self.document_types,
            }
        )


class DocumentRestrictionBuilder(object):
    def __init__(self):
        self.__country_codes = None
        self.__document_types = None

    def with_country_codes(self, country_codes):
        """
        Sets the list of country codes on the document restriction

        :param country_codes: the list of country codes
        :type country_codes: list[str]
        :return: the builder
        :rtype: DocumentRestrictionBuilder
        """
        self.__country_codes = country_codes
        return self

    def with_document_types(self, document_types):
        """
        Sets the list of document types on the document restriction

        :param document_types: the list of document types
        :type document_types: list[str]
        :return: the builder
        :rtype: DocumentRestrictionBuilder
        """
        self.__document_types = document_types
        return self

    def build(self):
        """
        Builds the document restriction using the values supplied to the builder

        :return: the document restriction
        :rtype: DocumentRestriction
        """
        return DocumentRestriction(self.__country_codes, self.__document_types)


class DocumentRestrictionsFilter(DocumentFilter):
    def __init__(self, inclusion, documents):
        DocumentFilter.__init__(self, DOCUMENT_RESTRICTIONS)

        self.__inclusion = inclusion
        self.__documents = documents

    @property
    def inclusion(self):
        return self.__inclusion

    @property
    def documents(self):
        return self.__documents

    def to_json(self):
        parent = DocumentFilter.to_json(self)
        parent["inclusion"] = self.inclusion
        parent["documents"] = self.documents
        return remove_null_values(parent)


class DocumentRestrictionsFilterBuilder(object):
    """
    Builder used to create a document restrictions filter.

    Example::

        document_restriction = (DocumentRestrictionBuilder()
                                .with_country_codes("GBR", "USA")
                                .with_document_types("PASSPORT")
                                .build())

        filter = (DocumentRestrictionsFilterBuilder()
                  .for_whitelist()
                  .with_document_restriction(document_restriction)
                  .build())
    """

    def __init__(self):
        self.__inclusion = None
        self.__documents = None

    def for_whitelist(self):
        """
        Sets the inclusion to whitelist the document restrictions

        :return: the builder
        :rtype: DocumentRestrictionsFilterBuilder
        """
        self.__inclusion = INCLUSION_WHITELIST
        return self

    def for_blacklist(self):
        """
        Sets the inclusion to blacklist the document restrictions

        :return: the builder
        :rtype: DocumentRestrictionsFilterBuilder
        """
        self.__inclusion = INCLUSION_BLACKLIST
        return self

    def with_document_restriction(self, document_restriction):
        """
        Adds a document restriction to the filter

        :param document_restriction: the document restriction
        :type document_restriction: DocumentRestriction
        :return: the builder
        :rtype: DocumentRestrictionsFilterBuilder
        """
        if self.__documents is None:
            self.__documents = []

        self.__documents.append(document_restriction)
        return self

    def build(self):
        """
        Builds the document restrictions filter, using the supplied values

        :return: the filter
        :rtype: DocumentRestrictionsFilter
        """
        return DocumentRestrictionsFilter(self.__inclusion, self.__documents)
