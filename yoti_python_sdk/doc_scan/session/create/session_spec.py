# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.utils import YotiSerializable


class SessionSpec(YotiSerializable):
    """
    Definition for the Doc Scan Session to be created
    """

    def __init__(
        self,
        client_session_token_ttl,
        resources_ttl,
        user_tracking_id,
        notifications,
        sdk_config,
        requested_checks=None,
        requested_tasks=None,
    ):
        """
        :param client_session_token_ttl: the client session token TTL
        :type client_session_token_ttl: int
        :param resources_ttl: the resources TTL
        :type resources_ttl: int
        :param user_tracking_id: the user tracking ID
        :type user_tracking_id: str
        :param notifications: the notification configuration
        :type notifications: NotificationConfig
        :param sdk_config: the SDK configuration
        :type sdk_config: SdkConfig
        :param requested_checks: the list of requested checks
        :type requested_checks: list[RequestedCheck]
        :param requested_tasks: the list of requested tasks
        :type requested_tasks: list[RequestedTask]
        """
        if requested_tasks is None:
            requested_tasks = []
        if requested_checks is None:
            requested_checks = []

        self.__client_session_token_ttl = client_session_token_ttl
        self.__resources_ttl = resources_ttl
        self.__user_tracking_id = user_tracking_id
        self.__notifications = notifications
        self.__sdk_config = sdk_config
        self.__requested_checks = requested_checks
        self.__requested_tasks = requested_tasks

    @property
    def client_session_token_ttl(self):
        """
        Client-session-token time-to-live to apply to the created Session

        :return: the client-session-token time-to-live
        :rtype: int
        """
        return self.__client_session_token_ttl

    @property
    def resources_ttl(self):
        """
        Time-to-live used for all Resources created in the course of the session

        :return: the time-to-live for Resources
        :rtype: int
        """
        return self.__resources_ttl

    @property
    def user_tracking_id(self):
        """
        User tracking ID, for the Relying Business to track returning users

        :return: the user tracking ID
        :rtype: str
        """
        return self.__user_tracking_id

    @property
    def notifications(self):
        """
        :class:`NotificationConfig` for configuring call-back messages

        :return: the notification config
        :rtype: NotificationConfig
        """
        return self.__notifications

    @property
    def sdk_config(self):
        """
        Retrieves the SDK configuration set of the session specification

        :return: the SDK config
        :rtype: SdkConfig
        """
        return self.__sdk_config

    @property
    def requested_checks(self):
        """
        List of :class:`RequestedCheck` objects defining the Checks to be performed
        on each Document

        :return: the requested checks
        :rtype: list[RequestedCheck]
        """
        return self.__requested_checks

    @property
    def requested_tasks(self):
        """
        List of :class:`RequestedTask` objects defining the Tasks to be performed
        on each Document

        :return: the requested tasks
        :rtype: list[RequestedTask]
        """
        return self.__requested_tasks

    def to_json(self):
        return {
            "client_session_token_ttl": self.client_session_token_ttl,
            "resources_ttl": self.resources_ttl,
            "user_tracking_id": self.user_tracking_id,
            "notifications": self.notifications,
            "requested_checks": self.requested_checks,
            "requested_tasks": self.requested_tasks,
            "sdk_config": self.sdk_config,
        }


class SessionSpecBuilder(object):
    """
    Builder to assist the creation of :class:`SessionSpec`
    """

    def __init__(self):
        self.__client_session_token_ttl = None
        self.__resources_ttl = None
        self.__user_tracking_id = None
        self.__notifications = None
        self.__sdk_config = None
        self.__requested_checks = []
        self.__requested_tasks = []

    def with_client_session_token_ttl(self, value):
        """
        Sets the client session token TTL (time-to-live)

        :param value: the client session token TTL
        :type value: int
        :return: the builder
        :rtype: SessionSpecBuilder
        """
        self.__client_session_token_ttl = value
        return self

    def with_resources_ttl(self, value):
        """
        Sets the resources TTL (time-to-live)

        :param value: the resources TTL
        :type value: int
        :return: the builder
        :rtype: SessionSpecBuilder
        """
        self.__resources_ttl = value
        return self

    def with_user_tracking_id(self, value):
        """
        Sets the user tracking ID

        :param value: the user tracking ID
        :type value: str
        :return: the builder
        :rtype: SessionSpecBuilder
        """
        self.__user_tracking_id = value
        return self

    def with_notifications(self, notifications):
        """
        Sets the notification configuration

        :param notifications: the notification config
        :type notifications: NotificationConfig
        :return: the builder
        :rtype: SessionSpecBuilder
        """
        self.__notifications = notifications
        return self

    def with_requested_check(self, check):
        """
        Adds a :class:`RequestedCheck` to the list

        :param check: the check to add
        :type check: RequestedCheck
        :return: the builder
        :rtype: SessionSpecBuilder
        """
        self.__requested_checks.append(check)
        return self

    def with_requested_task(self, task):
        """
        Adds a :class:`RequestedTask` to the list

        :param task: the task to add
        :type task: RequestedTask
        :return: the builder
        :rtype: SessionSpecBuilder
        """
        self.__requested_tasks.append(task)
        return self

    def with_sdk_config(self, value):
        """
        Sets the SDK configuration

        :param value: the SDK config
        :type value: SdkConfig
        :return: the builder
        :rtype: SessionSpecBuilder
        """
        self.__sdk_config = value
        return self

    def build(self):
        """
        Builds a :class:`SessionSpec` using the supplied values

        :return: the built Session Specification
        :rtype: SessionSpec
        """
        return SessionSpec(
            self.__client_session_token_ttl,
            self.__resources_ttl,
            self.__user_tracking_id,
            self.__notifications,
            self.__sdk_config,
            self.__requested_checks,
            self.__requested_tasks,
        )
