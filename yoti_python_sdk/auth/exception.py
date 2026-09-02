# -*- coding: utf-8 -*-
import json


class AuthException(Exception):
    """
    Exception thrown when an authentication token could not be generated
    """

    def __init__(self, message, response):
        """
        :param message: the exception message
        :type message: str
        :param response: the http response
        :type response: requests.Response
        """
        Exception.__init__(self)

        response_message = self.__get_response_message(response)

        self.__message = message + (
            " - " + response_message if response_message else ""
        )
        self.__response = response

    @property
    def message(self):
        """
        Get the specific exception message

        :return: the exception message
        :rtype: str
        """
        return self.__message

    @property
    def status_code(self):
        """
        Get the status code of the HTTP response

        :return: the status code
        :rtype: int or None
        """
        return self.__response.status_code

    @property
    def text(self):
        """
        Return the HTTP response body as text

        :return: the body as text
        :rtype: str
        """
        return self.__response.text

    def __get_response_message(self, response):
        """
        Return the formatted OAuth2 error response message

        :return: the formatted message
        :rtype: string or None
        """
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("application/json"):
            return None

        try:
            parsed = json.loads(response.text)
        except ValueError:
            return None

        return self.__format_oauth_error(parsed)

    @staticmethod
    def __format_oauth_error(parsed):
        """
        Return the formatted OAuth2 "error"/"error_description" message

        :return: the formatted message
        :rtype: string or None
        """
        error = parsed.get("error")
        if not error:
            return None

        description = parsed.get("error_description")
        if description:
            return error + " - " + description

        return error

    def __str__(self):
        return self.__message
