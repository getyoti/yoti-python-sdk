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

        self.__message = message
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

    def __str__(self):
        return self.__message
