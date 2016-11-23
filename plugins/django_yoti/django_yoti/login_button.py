from django.template.loader import render_to_string

from .settings import YOTI_APPLICATION_ID, YOTI_LOGIN_BUTTON_LABEL

LOGIN_BUTTON_SIZES = ('small', 'medium', 'large')


def get_login_button_html(size=None, text=YOTI_LOGIN_BUTTON_LABEL):
    size = size if size in LOGIN_BUTTON_SIZES else None
    return render_to_string('login_button.html', {
        'app_id': YOTI_APPLICATION_ID,
        'size': size,
        'text': text,
    })
