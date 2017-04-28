from flask import Markup

from .login_button import get_login_button_html
from .settings import get_config_value

def yoti_context():
    context = login_button_context()
    context.update(application_context())
    return context

def login_button_context():
    return {
        'yoti_login_button': get_login_button_html,
        'yoti_login_button_sm': get_login_button_html('small'),
        'yoti_login_button_md': get_login_button_html('medium'),
        'yoti_login_button_lg': get_login_button_html('large')
    }

def application_context():
    yoti_application_id = get_config_value('YOTI_APPLICATION_ID')
    return {'yoti_application_id': yoti_application_id}
