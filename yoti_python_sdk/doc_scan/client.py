# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import yoti_python_sdk
from yoti_python_sdk.doc_scan.endpoint import Endpoint
from yoti_python_sdk.doc_scan.session.retrieve.create_session_result import (
    CreateSessionResult,
)
from yoti_python_sdk.doc_scan.session.retrieve.get_session_result import (
    GetSessionResult,
)
from yoti_python_sdk.doc_scan.session.retrieve.media_value import MediaValue
from yoti_python_sdk.http import SignedRequest
from yoti_python_sdk.utils import YotiEncoder
from .exception import DocScanException
from .support import SupportedDocumentsResponse


class DocScanClient(object):
    """
    Client used for communication with the Yoti Doc Scan service where any
    signed request is required
    """

    def __init__(self, sdk_id, key, api_url=None):
        self.__sdk_id = sdk_id
        self.__key = key
        if api_url is not None:
            self.__api_url = api_url
        else:
            self.__api_url = yoti_python_sdk.YOTI_DOC_SCAN_API_URL

    def create_session(self, session_spec):
        """
        Creates a Doc Scan session using the supplied session specification

        :param session_spec: the session specification
        :type session_spec: SessionSpec
        :return: the create session result
        :rtype: CreateSessionResult
        :raises DocScanException: if there was an error creating the session
        """
        payload = json.dumps(session_spec, cls=YotiEncoder).encode("utf-8")

        request = (
            SignedRequest.builder()
            .with_post()
            .with_pem_file(self.__key)
            .with_base_url(self.__api_url)
            .with_endpoint(Endpoint.create_docs_session_path())
            .with_param("sdkId", self.__sdk_id)
            .with_payload(payload)
            .with_header("Content-Type", "application/json")
            .build()
        )
        response = request.execute()

        if response.status_code != 201:
            raise DocScanException("Failed to create session", response)

        data = json.loads(response.text)
        return CreateSessionResult(data)

    def get_session(self, session_id):
        """
        Retrieves the state of a previously created Yoti Doc Scan session

        :param session_id: the session ID
        :type session_id: str
        :return: the session state
        :rtype: GetSessionResult
        :raises DocScanException: if there was an error retrieving the session
        """
        request = (
            SignedRequest.builder()
            .with_get()
            .with_pem_file(self.__key)
            .with_base_url(self.__api_url)
            .with_endpoint(Endpoint.retrieve_docs_session_path(session_id))
            .with_param("sdkId", self.__sdk_id)
            .build()
        )
        response = request.execute()

        if response.status_code != 200:
            raise DocScanException("Failed to retrieve session", response)

        data = json.loads(response.text)
        return GetSessionResult(data)

    def delete_session(self, session_id):
        """
        Deletes a previously created Yoti Doc Scan session and
        all of its related resources

        :param session_id: the session id to delete
        :type session_id: str
        :rtype: None
        :raises DocScanException: if there was an error deleting the session
        """
        request = (
            SignedRequest.builder()
            .with_http_method("DELETE")
            .with_pem_file(self.__key)
            .with_base_url(self.__api_url)
            .with_endpoint(Endpoint.delete_docs_session_path(session_id))
            .with_param("sdkId", self.__sdk_id)
            .build()
        )
        response = request.execute()

        if response.status_code < 200 or response.status_code >= 300:
            raise DocScanException("Failed to delete session", response)

    def get_media_content(self, session_id, media_id):
        """
        Retrieves media related to a Yoti Doc Scan session
        based on the supplied media ID

        :param session_id: the session ID
        :type session_id: str
        :param media_id: the media ID
        :type media_id: str
        :return: the media
        :rtype: MediaValue
        :raises DocScanException: if there was an error retrieving the media content
        """
        request = (
            SignedRequest.builder()
            .with_get()
            .with_pem_file(self.__key)
            .with_base_url(self.__api_url)
            .with_endpoint(Endpoint.get_media_content_path(session_id, media_id))
            .with_param("sdkId", self.__sdk_id)
            .build()
        )
        response = request.execute()

        if response.status_code == 204:
            return None

        if response.status_code != 200:
            raise DocScanException("Failed to retrieve media content", response)

        media_mime_type = response.headers["Content-Type"]
        media_content = response.content
        return MediaValue(media_mime_type, media_content)

    def delete_media_content(self, session_id, media_id):
        """
        Deletes media related to a Yoti Doc Scan session
        based on the supplied media ID

        :param session_id: the session ID
        :type session_id: str
        :param media_id: the media ID
        :type media_id: str
        :rtype: None
        :raises DocScanException: if there was an error deleting the media content
        """
        request = (
            SignedRequest.builder()
            .with_http_method("DELETE")
            .with_pem_file(self.__key)
            .with_base_url(self.__api_url)
            .with_endpoint(Endpoint.delete_media_path(session_id, media_id))
            .with_param("sdkId", self.__sdk_id)
            .build()
        )

        response = request.execute()
        if response.status_code < 200 or response.status_code >= 300:
            raise DocScanException("Failed to delete media content", response)

    def get_supported_documents(self):
        """
        Retrieves a list of all of the currently supported documents

        :return: the supported documents response
        :rtype: SupportedDocumentsResponse
        """
        request = (
            SignedRequest.builder()
            .with_http_method("GET")
            .with_pem_file(self.__key)
            .with_base_url(self.__api_url)
            .with_endpoint(Endpoint.get_supported_documents_path())
            .build()
        )

        response = request.execute()
        if response.status_code < 200 or response.status_code >= 300:
            raise DocScanException("Failed to retrieve supported documents", response)

        parsed = json.loads(response.text)
        return SupportedDocumentsResponse(parsed)
