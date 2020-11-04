# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from deprecated import deprecated

from iso8601 import (
    ParseError,
    iso8601,
)

from yoti_python_sdk.doc_scan import constants
from .check_response import (
    AuthenticityCheckResponse,
    CheckResponse,
    FaceMatchCheckResponse,
    IDDocumentComparisonCheckResponse,
    LivenessCheckResponse,
    TextDataCheckResponse,
    SupplementaryDocumentTextDataCheckResponse,
)
from .resource_container import ResourceContainer


class GetSessionResult(object):
    """
    Represents all information about the state of a session
    at the time of the call, including check information,
    resources etc.
    """

    def __init__(self, data):
        """
        :param data: the data to parse
        :type data: dict
        """
        self.__client_session_token_ttl = data.get("client_session_token_ttl", None)
        self.__session_id = data.get("session_id", None)
        self.__user_tracking_id = data.get("user_tracking_id", None)
        self.__state = data.get("state", None)
        self.__client_session_token = data.get("client_session_token", None)
        self.__checks = [self.__parse_check(check) for check in data.get("checks", [])]
        self.__biometric_consent_timestamp = self.__parse_date(
            data.get("biometric_consent", None)
        )

        resources = data.get("resources", None)
        self.__resources = ResourceContainer(resources) or None

    @staticmethod
    def __parse_date(date):
        """
        Attempts to parse a date from string using the
        iso8601 library.  Returns None if there was an error

        :param date: the datestring to parse
        :type date: str
        :return: the parsed date
        :rtype: datetime.datetime or None
        """
        if date is None:
            return date

        try:
            return iso8601.parse_date(date)
        except ParseError:
            return None

    @staticmethod
    def __parse_check(check):
        """
        Parses a check into a sub-type of :class:`CheckResponse`,
        or falls back to CheckResponse if an unknown type

        :param check: the check object
        :type check: dict
        :return: the parsed check
        :rtype: CheckResponse
        """
        types = {
            constants.ID_DOCUMENT_AUTHENTICITY: AuthenticityCheckResponse,
            constants.ID_DOCUMENT_FACE_MATCH: FaceMatchCheckResponse,
            constants.ID_DOCUMENT_TEXT_DATA_CHECK: TextDataCheckResponse,
            constants.LIVENESS: LivenessCheckResponse,
            constants.ID_DOCUMENT_COMPARISON: IDDocumentComparisonCheckResponse,
            constants.SUPPLEMENTARY_DOCUMENT_TEXT_DATA_CHECK: SupplementaryDocumentTextDataCheckResponse,
        }
        clazz = types.get(check.get("type", None), CheckResponse)
        return clazz(check)

    @property
    def client_session_token_ttl(self):
        """
        The client session token time-to-live (TTL)

        :return: the client session token ttl
        :rtype: int or None
        """
        return self.__client_session_token_ttl

    @property
    def session_id(self):
        """
        The session ID

        :return: the session id
        :rtype: str or None
        """
        return self.__session_id

    @property
    def user_tracking_id(self):
        """
        The user tracking ID for the session

        :return: the user tracking id
        :rtype: str or None
        """
        return self.__user_tracking_id

    @property
    def state(self):
        """
        The state of the session, represented as a string e.g. "COMPLETED"

        :return: the state
        :rtype: str or None
        """
        return self.__state

    @property
    def client_session_token(self):
        """
        The client session token

        :return: the client session token
        :rtype: str or None
        """
        return self.__client_session_token

    @property
    def checks(self):
        """
        The list of Checks associated with the session

        :return: the list of Checks
        :rtype: list[CheckResponse]
        """
        return self.__checks

    def __checks_of_type(self, clazz):
        """
        Filter the list of checks by the class type

        :param clazz: the class
        :type clazz: tuple[type]
        :return:
        :rtype:
        """
        return [check for check in self.checks if isinstance(check, clazz)]

    @property
    def authenticity_checks(self):
        """
        A filtered list of checks, returning only document authenticity checks

        :return: the document authenticity checks
        :rtype: list[AuthenticityCheckResponse]
        """
        return self.__checks_of_type((AuthenticityCheckResponse,))

    @property
    def face_match_checks(self):
        """
        A filtered list of checks, returning only FaceMatch checks

        :return: the FaceMatch checks
        :rtype: list[FaceMatchCheckResponse]
        """
        return self.__checks_of_type((FaceMatchCheckResponse,))

    @property
    @deprecated("replaced by id_document_text_data_checks")
    def text_data_checks(self):
        """
        A filtered list of checks, returning only Text Data checks

        :return: the Text Data checks
        :rtype: list[TextDataCheckResponse]
        """
        return self.id_document_text_data_checks

    @property
    def id_document_text_data_checks(self):
        """
        A filtered list of checks, returning only ID Document Text Data checks

        :return: the Text Data checks
        :rtype: list[TextDataCheckResponse]
        """
        return self.__checks_of_type((TextDataCheckResponse,))

    @property
    def supplementary_document_text_data_checks(self):
        """
        A filtered list of checks, returning only Supplementary Document Text Data checks

        :return: the Text Data checks
        :rtype: list[SupplementaryDocumentTextDataCheckResponse]
        """
        return self.__checks_of_type((SupplementaryDocumentTextDataCheckResponse,))

    @property
    def liveness_checks(self):
        """
        A filtered list of checks, returning only Liveness checks

        :return: the Liveness checks
        :rtype: list[LivenessCheckResponse]
        """
        return self.__checks_of_type((LivenessCheckResponse,))

    @property
    def id_document_comparison_checks(self):
        """
        A filtered list of checks, returning only Identity Document Comparison checks

        :return: the Identity Document Comparison checks
        :rtype: list[IDDocumentComparisonCheckResponse]
        """
        return self.__checks_of_type((IDDocumentComparisonCheckResponse,))

    @property
    def resources(self):
        """
        The resources associated with the session

        :return: the resources
        :rtype: ResourceContainer or None
        """
        return self.__resources

    @property
    def biometric_consent_timestamp(self):
        """
        The biometric constent timestamp

        :return: the biometric constent timestamp
        :rtype: datetime.datetime or None
        """
        return self.__biometric_consent_timestamp
