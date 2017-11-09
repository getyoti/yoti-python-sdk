from django.test import TestCase

from ..context_processors import yoti_context


class TestContextProcessors(TestCase):
    def setUp(self):
        self.context = yoti_context(request=None)
        self.defaults = {
            'YOTI_APPLICATION_ID': '01234567-8901-2345-6789-012345678901',
            'YOTI_CLIENT_SDK_ID': '01234567-8901-2345-6789-012345678901',
            'YOTI_KEY_FILE_PATH': '/home/user/.ssh/yoti_key.pem',
        }

    def test_yoti_context(self):
        application_id_key = 'yoti_application_id'
        self.assert_(application_id_key in self.context.keys())

    def test_application_id(self):
        app_id = self.context.get('yoti_application_id')
        expected_app_id = self.defaults.get('YOTI_APPLICATION_ID')
        self.assertEqual(app_id, expected_app_id)
