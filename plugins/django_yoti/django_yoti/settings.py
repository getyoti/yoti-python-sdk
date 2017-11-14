from os import environ

from django.conf import settings

GLOBAL_YOTI_SETTINGS = getattr(settings, 'YOTI', {})


def _get_parameter(name, required=True):
    parameter = GLOBAL_YOTI_SETTINGS.get(name, environ.get(name))
    if parameter is None and required is True:
        raise RuntimeError(
            'Required parameter "{0}" is not set'.format(name)
        )
    return parameter


YOTI_APPLICATION_ID = _get_parameter('YOTI_APPLICATION_ID')
YOTI_CLIENT_SDK_ID = _get_parameter('YOTI_CLIENT_SDK_ID')
YOTI_KEY_FILE_PATH = _get_parameter('YOTI_KEY_FILE_PATH')

YOTI_REDIRECT_TO = GLOBAL_YOTI_SETTINGS.get('YOTI_REDIRECT_TO', 'yoti_profile')
YOTI_LOGIN_VIEW = GLOBAL_YOTI_SETTINGS.get('YOTI_LOGIN_VIEW', 'yoti_login')

__all__ = [
    'YOTI_APPLICATION_ID',
    'YOTI_CLIENT_SDK_ID',
    'YOTI_KEY_FILE_PATH',
    'YOTI_REDIRECT_TO',
    'YOTI_LOGIN_VIEW',
]
