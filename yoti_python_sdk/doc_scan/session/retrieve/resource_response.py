from yoti_python_sdk.doc_scan import constants
from .task_response import (
    TaskResponse,
    TextExtractionTaskResponse,
    SupplementaryDocumentTextExtractionTaskResponse,
)


class ResourceResponse(object):
    """
    Represents a resource
    """

    def __init__(self, data=None):
        """
        :param data: the data to parse
        :type data: dict or None
        """
        if data is None:
            data = dict()

        self.__id = data.get("id", None)
        self.__tasks = [self.__parse_task(task) for task in data.get("tasks", [])]

    @staticmethod
    def __parse_task(task):
        """
        Return a parsed task from a dictionary

        :param task: the raw task
        :type task: dict
        :return: the parsed task
        :rtype: TaskResponse
        """
        types = {
            constants.ID_DOCUMENT_TEXT_DATA_EXTRACTION: TextExtractionTaskResponse,
            constants.SUPPLEMENTARY_DOCUMENT_TEXT_DATA_EXTRACTION: SupplementaryDocumentTextExtractionTaskResponse,
        }
        clazz = types.get(
            task.get("type", None), TaskResponse  # Default fallback for task type
        )
        return clazz(task)

    @property
    def id(self):
        """
        The ID of the resource

        :return: the id
        :rtype: str
        """
        return self.__id

    @property
    def tasks(self):
        """
        Tasks associated with a resource

        :return: the list of tasks
        :rtype: list[TaskResponse]
        """
        return self.__tasks
