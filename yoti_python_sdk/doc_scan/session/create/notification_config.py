# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from yoti_python_sdk.doc_scan import constants
from yoti_python_sdk.doc_scan.constants import CHECK_COMPLETION
from yoti_python_sdk.doc_scan.constants import RESOURCE_UPDATE
from yoti_python_sdk.doc_scan.constants import SESSION_COMPLETION
from yoti_python_sdk.doc_scan.constants import TASK_COMPLETION
from yoti_python_sdk.utils import YotiSerializable, remove_null_values


class NotificationConfig(YotiSerializable):
    """
    Configures call-back Notifications to some backend endpoint provided by the Relying Business.

    Notifications can be configured to notify a clients backend of certain events, avoiding the need
    to poll for the state of the Session.
    """

    def __init__(self, auth_token, endpoint, topics=None, auth_type=None):
        """
        :param auth_token: the authorization token
        :type auth_token: str
        :param endpoint: the endpoint
        :type endpoint: str
        :param auth_type: authentication type (BASIC or BEARER)
        :type auth_type: str
        :param topics: the list of topics
        :type topics: list[str]
        """

        self.__auth_token = auth_token
        self.__endpoint = endpoint
        self.__auth_type = auth_type or constants.DocScanAuthType.BASIC.value
        self.__topics = list(set(topics or []))  # Get unique values

    @property
    def auth_token(self):
        """
        The authorization token to be included in call-back messages

        :return: the authorization token
        :rtype: str
        """
        return self.__auth_token

    @property
    def endpoint(self):
        """
        The endpoint that notifications should be sent to

        :return: the endpoint
        :rtype: str
        """
        return self.__endpoint

    @property
    def topics(self):
        """
        The list of topics that should trigger notifications

        :return: the list of topics
        :rtype: list[str]
        """
        return self.__topics

    @property
    def auth_type(self):
        """
        Auth type that notification should use

        :return: the auth_type
        :rtype: list[str]
        """
        return self.__auth_type

    def to_json(self):
        return remove_null_values(
            {
                "auth_type": self.auth_type,
                "auth_token": self.auth_token,
                "endpoint": self.endpoint,
                "topics": self.topics,
            }
        )


class NotificationConfigBuilder(object):
    """
    Builder to assist in the creation of :class:`NotificationConfig`
    """

    def __init__(self):
        self.__auth_type = None
        self.__auth_token = None
        self.__endpoint = None
        self.__topics = []

    def with_auth_type(self, auth_type):
        """
        Sets the auth_type to be included in call-back messages

        :param token: the auth_type (BASIC or BEARER)
        :type token: str
        :return: the builder
        :rtype: NotificationConfigBuilder
        """

        self.__auth_type = constants.DocScanAuthType(auth_type).value
        return self

    def with_auth_token(self, token):
        """
        Sets the authorization token to be included in call-back messages

        :param token: the authorization token
        :type token: str
        :return: the builder
        :rtype: NotificationConfigBuilder
        """
        self.__auth_token = token
        return self

    def with_endpoint(self, endpoint):
        """
        Sets the endpoint that notifications should be sent to

        :param endpoint: the endpoint
        :type endpoint: str
        :return: the builder
        :rtype: NotificationConfigBuilder
        """
        self.__endpoint = endpoint
        return self

    def with_topic(self, topic):
        """
        Adds a topic to the list of topics that trigger notification messages

        :param topic: the topic
        :type topic: str
        :return: the builder
        :rtype: NotificationConfigBuilder
        """

        self.__topics.append(topic)
        return self

    def for_resource_update(self):
        """
        Adds RESOURCE_UPDATE to the list of topics that trigger notification messages

        :return: the builder
        :rtype: NotificationConfigBuilder
        """
        return self.with_topic(RESOURCE_UPDATE)

    def for_task_completion(self):
        """
        Adds TASK_COMPLETION to the list of topics that trigger notification messages

        :return: the builder
        :rtype: NotificationConfigBuilder
        """
        return self.with_topic(TASK_COMPLETION)

    def for_session_completion(self):
        """
        Adds SESSION_COMPLETION to the list of topics that trigger notification messages

        :return: the builder
        :rtype: NotificationConfigBuilder
        """
        return self.with_topic(SESSION_COMPLETION)

    def for_check_completion(self):
        """
        Adds CHECK_COMPLETION to the list of topics that trigger notification messages

        :return: the builder
        :rtype: NotificationConfigBuilder
        """
        return self.with_topic(CHECK_COMPLETION)

    def build(self):
        """
        Builds the :class:`NotificationConfig` using the supplied values

        :return: the build notification config
        :rtype: NotificationConfig
        """
        return NotificationConfig(self.__auth_token, self.__endpoint, self.__topics, self.__auth_type,)
