# -*- coding: utf-8 -*-


class CreateAuthenticationTokenResponse(object):
    """
    The response returned when generating a central auth token
    """

    def __init__(self, data):
        """
        :param data: the parsed JSON response body
        :type data: dict
        """
        self.__access_token = data.get("access_token")
        self.__token_type = data.get("token_type")
        self.__expires_in = data.get("expires_in")
        self.__scope = data.get("scope")

    @property
    def access_token(self):
        """
        The auth token to be supplied to an SDK client

        :return: the access token
        :rtype: str
        """
        return self.__access_token

    @property
    def token_type(self):
        """
        The type of token issued, e.g. "Bearer"

        :return: the token type
        :rtype: str
        """
        return self.__token_type

    @property
    def expires_in(self):
        """
        The lifetime of the access token in seconds.  The SDK does not
        automatically refresh the token on expiry; it is the caller's
        responsibility to generate a new one before it expires

        :return: the expiry, in seconds
        :rtype: int or None
        """
        return self.__expires_in

    @property
    def scope(self):
        """
        The scopes granted to the access token

        :return: the granted scopes
        :rtype: str or None
        """
        return self.__scope
