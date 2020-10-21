import json


class DocScanException(Exception):
    """
    Exception thrown by the Yoti Doc Scan client
    when an error has occurred when communicating with the API
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

    @property
    def content(self):
        """
        Return the HTTP response body as bytes

        :return: the body as bytes
        :rtype: bytearray or None
        """
        return self.__response.content

    def __get_response_message(self, response):
        """
        Return the formatted response message

        :return: the formatted message
        :rtype: string or None
        """
        if response.headers.get("Content-Type") == "application/json":
            return self.__format_json_response_message(json.loads(response.text))

        return None

    def __format_json_response_message(self, parsed):
        """
        Return the formatted JSON response message

        :return: the formatted message
        :rtype: string or None
        """
        if not parsed.get("code") or not parsed.get("message"):
            return None

        code_message = parsed.get("code") + " - " + parsed.get("message")

        errors = []
        for error in parsed.get("errors", []):
            if error.get("property") and error.get("message"):
                errors.append(error.get("property") + ' "' + error.get("message") + '"')

        if len(errors) > 0:
            return code_message + ": " + ", ".join(errors)

        return code_message

    def __str__(self):
        return self.__message
