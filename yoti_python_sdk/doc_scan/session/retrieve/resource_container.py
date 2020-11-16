# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.doc_scan.session.retrieve.id_document_resource_response import (
    IdDocumentResourceResponse,
)
from yoti_python_sdk.doc_scan.session.retrieve.supplementary_document_resource_response import (
    SupplementaryDocumentResourceResponse,
)
from yoti_python_sdk.doc_scan.session.retrieve.liveness_resource_response import (
    LivenessResourceResponse,
    ZoomLivenessResourceResponse,
)


class ResourceContainer(object):
    """
    Contains different resources that are part of the Yoti
    Doc Scan session
    """

    def __init__(self, data=None):
        """
        :param data: the data to parse
        :type data: dict or None
        """
        if data is None:
            data = dict()

        self.__id_documents = [
            IdDocumentResourceResponse(document)
            for document in data.get("id_documents", [])
        ]

        self.__supplementary_documents = [
            SupplementaryDocumentResourceResponse(document)
            for document in data.get("supplementary_documents", [])
        ]

        self.__liveness_capture = [
            self.__parse_liveness_capture(liveness)
            for liveness in data.get("liveness_capture", [])
        ]

    @staticmethod
    def __parse_liveness_capture(liveness_capture):
        """
        Parses a liveness capture into a specific sub-class based on the
        liveness type.  If no liveness type is available, it falls back
        to the parent class :class:`LivenessResourceResponse`

        :param liveness_capture: the liveness capture
        :type liveness_capture: dict
        :return: the parsed liveness capture
        :rtype: LivenessResourceResponse
        """
        types = {"ZOOM": ZoomLivenessResourceResponse}

        clazz = types.get(
            liveness_capture.get("liveness_type", None),
            LivenessResourceResponse,  # Fallback value for unknown type
        )
        return clazz(liveness_capture)

    @property
    def id_documents(self):
        """
        Return a list of ID document resources

        :return: list of ID documents
        :rtype: list[IdDocumentResourceResponse]
        """
        return self.__id_documents

    @property
    def supplementary_documents(self):
        """
        Return a list of supplementary document resources

        :return: list of supplementary documents
        :rtype: list[SupplementaryDocumentResourceResponse]
        """
        return self.__supplementary_documents

    @property
    def liveness_capture(self):
        """
        Return a list of liveness capture resources

        :return: list of liveness captures
        :rtype: list[LivenessResourceResponse]
        """
        return self.__liveness_capture

    @property
    def zoom_liveness_resources(self):
        """
        Returns a filtered list of zoom liveness capture resources

        :return: list of zoom liveness captures
        :rtype: list[ZoomLivenessResourceResponse]
        """
        return [
            liveness
            for liveness in self.__liveness_capture
            if isinstance(liveness, ZoomLivenessResourceResponse)
        ]
