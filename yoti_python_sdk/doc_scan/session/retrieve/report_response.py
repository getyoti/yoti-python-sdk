from .breakdown_response import BreakdownResponse
from .recommendation_response import RecommendationResponse


class ReportResponse(object):
    """
    Represents a report for a given check
    """

    def __init__(self, data=None):
        """
        :param data: the data to parse
        :type data: dict or None
        """
        if data is None:
            data = dict()

        self.__recommendation = (
            RecommendationResponse(data["recommendation"])
            if "recommendation" in data.keys()
            else None
        )

        self.__breakdown = [
            BreakdownResponse(breakdown) for breakdown in data.get("breakdown", [])
        ]

    @property
    def recommendation(self):
        """
        The recommendation given for a given check/task

        :return: the recommendation
        :rtype: RecommendationResponse
        """
        return self.__recommendation

    @property
    def breakdown(self):
        """
        A list of breakdowns for different sub-checks performed

        :return: the list of breakdowns
        :rtype: list[BreakdownResponse]
        """
        return self.__breakdown
