class RecommendationResponse(object):
    """
    Represents the recommendation given for a check
    """

    def __init__(self, data=None):
        """
        :param data: the data to parse
        :type data: dict or None
        """
        if data is None:
            data = dict()

        self.__value = data.get("value", None)
        self.__reason = data.get("reason", None)
        self.__recovery_suggestion = data.get("recovery_suggestion", None)

    @property
    def value(self):
        """
        Returns the value of the recommendation

        :return: the value
        :rtype: str or None
        """
        return self.__value

    @property
    def reason(self):
        """
        Returns the reason of the recommendation

        :return: the reason
        :rtype: str or None
        """
        return self.__reason

    @property
    def recovery_suggestion(self):
        """
        Returns the recovery suggestion of the recommendation

        :return: the recovery suggestion
        :rtype: str or None
        """
        return self.__recovery_suggestion
