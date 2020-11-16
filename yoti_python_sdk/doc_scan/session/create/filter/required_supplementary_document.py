from yoti_python_sdk.doc_scan.constants import SUPPLEMENTARY_DOCUMENT
from yoti_python_sdk.utils import remove_null_values
from .required_document import RequiredDocument


class RequiredSupplementaryDocument(RequiredDocument):
    def __init__(self, objective, document_types=None, country_codes=None):
        """
        :param objective: the objective for the document
        :type objective: Objective
        :param document_types: the document types
        :type document_types: list[str]
        :param country_codes: the country codes
        :type country_codes: list[str]
        """
        self.__objective = objective
        self.__document_types = document_types
        self.__country_codes = country_codes

    @property
    def type(self):
        return SUPPLEMENTARY_DOCUMENT

    def to_json(self):
        return remove_null_values(
            {
                "type": self.type,
                "objective": self.__objective,
                "document_types": self.__document_types,
                "country_codes": self.__country_codes,
            }
        )


class RequiredSupplementaryDocumentBuilder(object):
    """
    Builder used to assist the creation of a required supplementary document.
    """

    def __init__(self):
        self.__objective = None
        self.__document_types = None
        self.__country_codes = None

    def with_objective(self, objective):
        """
        Sets the supplementary document objective

        :param objective: the objective
        :type objective: Objective
        :return: the builder
        :rtype: RequiredSupplementaryDocumentBuilder
        """
        self.__objective = objective
        return self

    def with_document_types(self, document_types):
        """
        Sets the supplementary document types

        :param document_types: the document types
        :type document_types: list[str]
        :return: the builder
        :rtype: RequiredSupplementaryDocumentBuilder
        """
        self.__document_types = document_types
        return self

    def with_country_codes(self, country_codes):
        """
        Sets the supplementary document country codes

        :param country_codes: the country codes
        :type country_codes: list[str]
        :return: the builder
        :rtype: RequiredSupplementaryDocumentBuilder
        """
        self.__country_codes = country_codes
        return self

    def build(self):
        """
        Builds a required supplementary document, using the values supplied to the builder

        :return: the required supplementary document
        :rtype: RequiredSupplementaryDocument
        """
        return RequiredSupplementaryDocument(
            self.__objective, self.__document_types, self.__country_codes
        )
