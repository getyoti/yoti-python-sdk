from django.test import TestCase

from ..context_processors import yoti_context
from ..login_button import get_login_button_html


class TestContextProcessors(TestCase):

    def setUp(self):
        self.context = yoti_context(request=None)
        self.defaults = {
            'YOTI_APPLICATION_ID': '01234567-8901-2345-6789-012345678901',
            'YOTI_CLIENT_SDK_ID': '01234567-8901-2345-6789-012345678901',
            'YOTI_VERIFICATION_KEY': '0123456789012345',
            'YOTI_KEY_FILE_PATH': '/home/user/.ssh/yoti_key.pem',
            'YOTI_LOGIN_BUTTON_LABEL': 'Test label'
        }

    def test_yoti_context(self):
        keys = ('yoti_application_id', 'yoti_site_verification',
                'yoti_login_button', 'yoti_login_button_sm',
                'yoti_login_button_md', 'yoti_login_button_lg')
        assert set(self.context.keys()) == set(keys)

    def test_application_id(self):
        app_id = self.context.get('yoti_application_id')
        expected_app_id = self.defaults.get('YOTI_APPLICATION_ID')
        assert app_id == expected_app_id

    def test_verification_key(self):
        context_tag = self.context.get('yoti_site_verification')
        html = '<meta name="yoti-site-verification" content="{0}">'.format(
            self.defaults.get('YOTI_VERIFICATION_KEY')
        )
        self.assertHTMLEqual(context_tag, html)

    def test_predefined_login_buttons(self):
        context = self.context
        assert 'data-size="small"' in context.get('yoti_login_button_sm')
        assert 'data-size="medium"' in context.get('yoti_login_button_md')
        assert 'data-size="large"' in context.get('yoti_login_button_lg')

    def test_login_button_func(self):
        app_id = self.defaults.get('YOTI_APPLICATION_ID')
        button_label = self.defaults.get('YOTI_LOGIN_BUTTON_LABEL')
        login_button_func = self.context.get('yoti_login_button')
        assert hasattr(login_button_func, '__call__')
        button_html = login_button_func(text=button_label)
        expected = '<span data-yoti-application-id="{0}" >' \
                   '{1}</span>'.format(app_id, button_label)
        assert button_html == expected

    def test_context_login_button_func_with_different_sizes(self):
        for size in ('small', 'medium', 'large'):
            button_html = get_login_button_html(size)
            assert 'data-size="{0}"'.format(size) in button_html
