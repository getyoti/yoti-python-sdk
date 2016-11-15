from django.utils.html import format_html
from .settings import YOTI_APPLICATION_ID, YOTI_LOGIN_BUTTON_LABEL

LOGIN_BUTTON_SIZES = ('small', 'medium', 'large')


def get_login_button_html(size=None, text=YOTI_LOGIN_BUTTON_LABEL):
    if size and size not in LOGIN_BUTTON_SIZES:
        size = None
    data_size = 'data-size="{0}"'.format(size) if size else ''
    raw_text = '<span data-yoti-application-id="{0}" {1}>' \
               '{2}</span>'.format(YOTI_APPLICATION_ID, data_size, text)
    return format_html(raw_text)
