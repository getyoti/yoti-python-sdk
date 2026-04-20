# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.doc_scan import constants
from yoti_python_sdk.utils import YotiSerializable
from .requested_task import RequestedTask


class RequestedFaceCaptureTaskConfig(YotiSerializable):
    """
    The configuration applied when creating a Face Capture Task
    """

    def to_json(self):
        return {}


class RequestedFaceCaptureTask(RequestedTask):
    """
    Requests creation of a Face Capture Task
    """

    def __init__(self, config):
        """
        :param config: the face capture task configuration
        :type config: RequestedFaceCaptureTaskConfig
        """
        self.__config = config

    @property
    def type(self):
        return constants.FACE_CAPTURE

    @property
    def config(self):
        return self.__config


class RequestedFaceCaptureTaskBuilder(object):
    """
    Builder to assist creation of :class:`RequestedFaceCaptureTask`
    """

    @staticmethod
    def build():
        config = RequestedFaceCaptureTaskConfig()
        return RequestedFaceCaptureTask(config)
