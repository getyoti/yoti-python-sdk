from os import environ

from flask import current_app


def get_default_value(name):
    return {
        'YOTI_APPLICATION_ID': environ.get('YOTI_APPLICATION_ID'),
        'YOTI_CLIENT_SDK_ID': environ.get('YOTI_CLIENT_SDK_ID'),
        'YOTI_KEY_FILE_PATH': environ.get('YOTI_KEY_FILE_PATH'),
        'YOTI_REDIRECT_TO': 'flask_yoti.profile',
        'YOTI_LOGIN_VIEW': 'flask_yoti.login',
        'YOTI_LOGIN_BUTTON_LABEL': 'Log in with Yoti'
    }.get(name)


def get_config_value(name):
    try:
        config = current_app.config
        parameter = config.get(name, get_default_value(name))
    except RuntimeError:
        parameter = get_default_value(name)

    if parameter is None:
        raise RuntimeError(
            'Required parameter "{0}" is not configured'.format(name)
        )
    return parameter
