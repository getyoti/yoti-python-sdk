from flask import Markup

from .settings import get_config_value

LOGIN_BUTTON_SIZES = ('small', 'medium', 'large')


def get_login_button_html(size=None, text=None, app_id=None):
    text = text or get_config_value('YOTI_LOGIN_BUTTON_LABEL')
    app_id = app_id or get_config_value('YOTI_APPLICATION_ID')

    if size and size not in LOGIN_BUTTON_SIZES:
        size = None
    data_size = 'data-size="{0}"'.format(size) if size else ''

    raw_text = '<span data-yoti-application-id="{0}" {1}>' \
               '{2}</span>'.format(app_id, data_size, text)
    return Markup(raw_text)
