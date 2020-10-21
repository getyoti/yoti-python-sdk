# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.doc_scan.session.retrieve.document_fields_response import (
    DocumentFieldsResponse,
)
from yoti_python_sdk.doc_scan.session.retrieve.document_id_photo_response import (
    DocumentIdPhotoResponse,
)
from yoti_python_sdk.doc_scan.session.retrieve.page_response import PageResponse
from yoti_python_sdk.doc_scan.session.retrieve.resource_response import ResourceResponse
from yoti_python_sdk.doc_scan.session.retrieve.task_response import (
    TextExtractionTaskResponse,
)


class IdDocumentResourceResponse(ResourceResponse):
    """
    Represents an Identity Document resource for a given session
    """

    def __init__(self, data=None):
        """
        :param data: the data to parse
        :type data: dict or None
        """
        if data is None:
            data = dict()

        ResourceResponse.__init__(self, data)

        self.__document_type = data.get("document_type", None)
        self.__issuing_country = data.get("issuing_country", None)
        self.__pages = [PageResponse(page) for page in data.get("pages", [])]
        self.__document_fields = (
            DocumentFieldsResponse(data["document_fields"])
            if "document_fields" in data.keys()
            else None
        )
        self.__document_id_photo = (
            DocumentIdPhotoResponse(data["document_id_photo"])
            if "document_id_photo" in data.keys()
            else None
        )

    @property
    def document_type(self):
        """
        Returns the identity document type, e.g. "PASSPORT"

        :return: the document type
        :rtype: str or None
        """
        return self.__document_type

    @property
    def issuing_country(self):
        """
        Returns the issuing country of the identity document

        :return: the issuing country
        :rtype: str or None
        """
        return self.__issuing_country

    @property
    def pages(self):
        """
        Returns the individual pages of the identity document

        :return: the pages
        :rtype: list[PageResponse]
        """
        return self.__pages

    @property
    def document_fields(self):
        """
        Returns the associated document fields

        :return: the document fields
        :rtype: DocumentFieldsResponse
        """
        return self.__document_fields

    @property
    def document_id_photo(self):
        """
        Returns the associated document ID photo

        :return: the document ID photo
        :rtype: DocumentIdPhotoResponse
        """
        return self.__document_id_photo

    @property
    def text_extraction_tasks(self):
        """
        Returns a list of text extraction tasks associated
        with the identity document

        :return: list of text extraction tasks
        :rtype: list[TextExtractionTaskResponse]
        """
        return [
            task for task in self.tasks if isinstance(task, TextExtractionTaskResponse)
        ]
