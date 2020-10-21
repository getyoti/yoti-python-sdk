from yoti_python_sdk.doc_scan.constants import INCLUSION_BLACKLIST
from yoti_python_sdk.doc_scan.constants import INCLUSION_WHITELIST
from yoti_python_sdk.doc_scan.constants import ORTHOGONAL_RESTRICTIONS
from yoti_python_sdk.utils import YotiSerializable, remove_null_values
from .document_filter import DocumentFilter


class CountryRestriction(YotiSerializable):
    def __init__(self, inclusion, country_codes):
        self.__inclusion = inclusion
        self.__country_codes = country_codes

    @property
    def inclusion(self):
        """
        Returns the inclusion for the country restriction

        :return: the inclusion
        :rtype: str
        """
        return self.__inclusion

    @property
    def country_codes(self):
        """
        Returns the country codes for the restriction

        :return: the country codes
        :rtype: list[str]
        """
        return self.__country_codes

    def to_json(self):
        return remove_null_values(
            {"inclusion": self.inclusion, "country_codes": self.country_codes}
        )


class TypeRestriction(YotiSerializable):
    def __init__(self, inclusion, document_types):
        self.__inclusion = inclusion
        self.__document_types = document_types

    @property
    def inclusion(self):
        """
        Returns the inclusion for the type restriction

        :return: the inclusion
        :rtype: str
        """
        return self.__inclusion

    @property
    def document_types(self):
        """
        Returns the document types for the restriction

        :return: the document types
        :rtype: list[str]
        """
        return self.__document_types

    def to_json(self):
        return remove_null_values(
            {"inclusion": self.inclusion, "document_types": self.document_types}
        )


class OrthogonalRestrictionsFilter(DocumentFilter):
    def __init__(self, country_restriction, type_restriction):
        DocumentFilter.__init__(self, filter_type=ORTHOGONAL_RESTRICTIONS)

        self.__country_restriction = country_restriction
        self.__type_restriction = type_restriction

    @property
    def country_restriction(self):
        """
        Returns the country restriction for the orthogonal filter

        :return: the country restriction
        :rtype: CountryRestriction
        """
        return self.__country_restriction

    @property
    def type_restriction(self):
        """
        Returns the document type restriction for the orthogonal filter

        :return: the document type restriction
        :rtype: TypeRestriction
        """
        return self.__type_restriction

    def to_json(self):
        parent = DocumentFilter.to_json(self)
        parent["country_restriction"] = self.country_restriction
        parent["type_restriction"] = self.type_restriction
        return remove_null_values(parent)


class OrthogonalRestrictionsFilterBuilder(object):
    """
    Builder used to create an orthogonal restriction filter.

    Example::

        filter = (OrthogonalRestrictionsFilterBuilder()
                  .with_whitelisted_country_codes(["GBR", "USA"])
                  .with_whitelisted_document_types(["PASSPORT"])
                  .build())

    """

    def __init__(self):
        self.__country_restriction = None
        self.__type_restriction = None

    def with_whitelisted_country_codes(self, country_codes):
        """
        Sets a whitelisted list of country codes on the filter

        :param country_codes: List of country codes
        :type country_codes: list[str]
        :return: the builder
        :rtype: OrthogonalRestrictionsFilterBuilder
        """
        self.__country_restriction = CountryRestriction(
            INCLUSION_WHITELIST, country_codes
        )
        return self

    def with_blacklisted_country_codes(self, country_codes):
        """
        Sets a blacklisted list of country codes on the filter

        :param country_codes: list of country codes
        :type country_codes: list[str]
        :return: the builder
        :rtype: OrthogonalRestrictionsFilterBuilder
        """
        self.__country_restriction = CountryRestriction(
            INCLUSION_BLACKLIST, country_codes
        )
        return self

    def with_whitelisted_document_types(self, document_types):
        """
        Sets a whitelisted list of document types on the filter

        :param document_types: list of document types
        :type document_types: list[str]
        :return: the builder
        :rtype: OrthogonalRestrictionsFilterBuilder
        """
        self.__type_restriction = TypeRestriction(INCLUSION_WHITELIST, document_types)
        return self

    def with_blacklisted_document_types(self, document_types):
        """
        Sets a blacklisted list of document types on the filter

        :param document_types: list of document types
        :type document_types: list[str]
        :return: the builder
        :rtype: OrthogonalRestrictionsFilterBuilder
        """
        self.__type_restriction = TypeRestriction(INCLUSION_BLACKLIST, document_types)
        return self

    def build(self):
        """
        Builds the orthogonal filter, using the supplied whitelisted/blacklisted values

        :return: the built filter
        :rtype: OrthogonalRestrictionsFilter
        """
        return OrthogonalRestrictionsFilter(
            self.__country_restriction, self.__type_restriction
        )
