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
from yoti_python_sdk.doc_scan.session.retrieve.static_liveness_resource_response import (
    StaticLivenessResourceResponse,
)
from yoti_python_sdk.doc_scan.session.retrieve.share_code_resource_response import (
    ShareCodeResourceResponse,
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

        self.__share_codes = [
            ShareCodeResourceResponse(share_code)
            for share_code in data.get("share_codes", [])
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
        types = {"ZOOM": ZoomLivenessResourceResponse, "STATIC": StaticLivenessResourceResponse}

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

    @property
    def static_liveness_resources(self):
        """
        Returns a filtered list of static liveness capture resources

        :return: list of static liveness captures
        :rtype: list[StaticLivenessResourceResponse]
        """
        return [
            liveness
            for liveness in self.__liveness_capture
            if isinstance(liveness, StaticLivenessResourceResponse)
        ]

    @property
    def share_codes(self):
        """
        Return a list of share code resources

        :return: list of share codes
        :rtype: list[ShareCodeResourceResponse]
        """
        return self.__share_codes

    def filter_for_check(self, check_response):
        """
        Returns a new ResourceContainer containing only the resources
        referenced by the given check's resources_used

        :param check_response: the check to filter resources for
        :type check_response: yoti_python_sdk.doc_scan.session.retrieve.check_response.CheckResponse
        :return: a ResourceContainer containing only the resources used by the check
        :rtype: ResourceContainer
        """
        resource_ids = set(check_response.resources_used)

        filtered = ResourceContainer()
        filtered.__id_documents = self.__filter_resources(
            self.__id_documents, resource_ids
        )
        filtered.__supplementary_documents = self.__filter_resources(
            self.__supplementary_documents, resource_ids
        )
        filtered.__liveness_capture = self.__filter_resources(
            self.__liveness_capture, resource_ids
        )
        filtered.__share_codes = self.__filter_resources(
            self.__share_codes, resource_ids
        )
        return filtered

    @staticmethod
    def __filter_resources(resources, resource_ids):
        return [resource for resource in resources if resource.id in resource_ids]
