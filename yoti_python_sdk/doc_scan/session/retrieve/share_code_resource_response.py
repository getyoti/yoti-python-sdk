from yoti_python_sdk.doc_scan.session.retrieve.resource_response import (
    ResourceResponse,
)
from yoti_python_sdk.doc_scan.session.retrieve.share_code_media_response import (
    ShareCodeMediaResponse,
)
from yoti_python_sdk.doc_scan.session.retrieve.verify_share_code_task_response import (
    VerifyShareCodeTaskResponse,
)


class ShareCodeResourceResponse(ResourceResponse):
    """
    Represents a share code resource for a given session
    """

    def __init__(self, data=None):
        if data is None:
            data = dict()

        ResourceResponse.__init__(self, data)

        source = data.get("source", None)
        if isinstance(source, str):
            self.__source = source
        elif isinstance(source, dict):
            self.__source = source.get("type", None)
        else:
            self.__source = None

        self.__created_at = data.get("created_at", None)
        self.__last_updated = data.get("last_updated", None)

        self.__lookup_profile = (
            ShareCodeMediaResponse(data["lookup_profile"])
            if "lookup_profile" in data and data["lookup_profile"] is not None
            else None
        )
        self.__returned_profile = (
            ShareCodeMediaResponse(data["returned_profile"])
            if "returned_profile" in data and data["returned_profile"] is not None
            else None
        )
        self.__id_photo = (
            ShareCodeMediaResponse(data["id_photo"])
            if "id_photo" in data and data["id_photo"] is not None
            else None
        )
        self.__file = (
            ShareCodeMediaResponse(data["file"])
            if "file" in data and data["file"] is not None
            else None
        )

    @property
    def source(self):
        """
        The source of the share code

        :return: the source
        :rtype: str or None
        """
        return self.__source

    @property
    def created_at(self):
        """
        The date the share code was created

        :return: the created at date
        :rtype: str or None
        """
        return self.__created_at

    @property
    def last_updated(self):
        """
        The date the share code was last updated

        :return: the last updated date
        :rtype: str or None
        """
        return self.__last_updated

    @property
    def lookup_profile(self):
        """
        The lookup profile media

        :return: the lookup profile
        :rtype: ShareCodeMediaResponse or None
        """
        return self.__lookup_profile

    @property
    def returned_profile(self):
        """
        The returned profile media

        :return: the returned profile
        :rtype: ShareCodeMediaResponse or None
        """
        return self.__returned_profile

    @property
    def id_photo(self):
        """
        The ID photo media

        :return: the ID photo
        :rtype: ShareCodeMediaResponse or None
        """
        return self.__id_photo

    @property
    def file(self):
        """
        The file media

        :return: the file
        :rtype: ShareCodeMediaResponse or None
        """
        return self.__file

    @property
    def verify_share_code_tasks(self):
        """
        Returns a list of verify share code tasks

        :return: list of verify share code tasks
        :rtype: list[VerifyShareCodeTaskResponse]
        """
        return [
            task
            for task in self.tasks
            if isinstance(task, VerifyShareCodeTaskResponse)
        ]
