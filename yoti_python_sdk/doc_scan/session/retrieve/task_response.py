# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import iso8601
from iso8601 import ParseError

from yoti_python_sdk.doc_scan import constants
from yoti_python_sdk.doc_scan.session.retrieve.generated_check_response import (
    GeneratedCheckResponse,
    GeneratedTextDataCheckResponse,
    GeneratedSupplementaryDocumentTextDataCheckResponse,
)
from yoti_python_sdk.doc_scan.session.retrieve.generated_media import GeneratedMedia


class TaskResponse(object):
    """
    Represents a task
    """

    def __init__(self, data=None):
        """
        :param data: the data to parse
        :type data: dict or None
        """
        if data is None:
            data = dict()

        self.__id = data.get("id", None)
        self.__type = data.get("type", None)
        self.__state = data.get("state", None)

        self.__created = self.__parse_date(data.get("created", None))
        self.__last_updated = self.__parse_date(data.get("last_updated", None))

        self.__generated_checks = [
            self.__parse_generated_check(check)
            for check in data.get("generated_checks", [])
        ]
        self.__generated_media = [
            GeneratedMedia(media) for media in data.get("generated_media", [])
        ]

    @staticmethod
    def __parse_generated_check(generated_check):
        """
        Parse a generated check into an object from a dict
        :param generated_check: the raw generated check
        :type generated_check: dict
        :return: the parse generated check
        :rtype: GeneratedCheckResponse
        """
        types = {
            constants.ID_DOCUMENT_TEXT_DATA_CHECK: GeneratedTextDataCheckResponse,
            constants.SUPPLEMENTARY_DOCUMENT_TEXT_DATA_CHECK: GeneratedSupplementaryDocumentTextDataCheckResponse,
        }

        clazz = types.get(
            generated_check.get("type", None),
            GeneratedCheckResponse,  # Default fallback for type
        )
        return clazz(generated_check)

    @staticmethod
    def __parse_date(date):
        """
        Parse a date using the iso8601 library,
        returning None if there was an error

        :param date: the date string to parse
        :type date: str
        :return: the parse date
        :rtype: datetime.datetime or None
        """
        if date is None:
            return None

        try:
            return iso8601.parse_date(date)
        except ParseError:
            return None

    @property
    def type(self):
        """
        Return the type of the task

        :return: the type
        :rtype: str or None
        """
        return self.__type

    @property
    def id(self):
        """
        Return the ID of the task

        :return: the ID
        :rtype: str or None
        """
        return self.__id

    @property
    def state(self):
        """
        Return the state of the task

        :return: the state
        :rtype: str or None
        """
        return self.__state

    @property
    def created(self):
        """
        Return the date the task was created

        :return: the created date
        :rtype: datetime.datetime or None
        """
        return self.__created

    @property
    def last_updated(self):
        """
        Return the date the task was last updated

        :return: the last updated date
        :rtype: datetime.datetime or None
        """
        return self.__last_updated

    @property
    def generated_checks(self):
        """
        Return the list of checks that were generated
        by the task

        :return: the generated checks
        :rtype: list[GeneratedCheckResponse]
        """
        return self.__generated_checks

    @property
    def generated_media(self):
        """
        Return the list of media that has been generated
        by the task

        :return: the list of generated media
        :rtype: list[GeneratedMedia]
        """
        return self.__generated_media


class TextExtractionTaskResponse(TaskResponse):
    """
    Represents an ID Document Text Extraction task response
    """

    @property
    def generated_text_data_checks(self):
        return [
            check
            for check in self.generated_checks
            if isinstance(check, GeneratedTextDataCheckResponse)
        ]


class SupplementaryDocumentTextExtractionTaskResponse(TaskResponse):
    """
    Represents a Supplementary Document Text Extraction task response
    """

    @property
    def generated_text_data_checks(self):
        return [
            check
            for check in self.generated_checks
            if isinstance(check, GeneratedSupplementaryDocumentTextDataCheckResponse)
        ]
