import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

# https://docs.djangoproject.com/el/1.10/topics/testing/advanced/
if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        ROOT_URLCONF='django_yoti.urls',
        INSTALLED_APPS=('django_yoti',
                        'django.contrib.admin',
                        'django.contrib.auth',
                        'django.contrib.contenttypes',
                        'django.contrib.sessions',
                        'django.contrib.messages',
                        'django.contrib.staticfiles'),
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django_yoti.context_processors.yoti_context',
                    ],
                },
            },
        ],
        YOTI={
            'YOTI_APPLICATION_ID': '01234567-8901-2345-6789-012345678901',
            'YOTI_CLIENT_SDK_ID': '01234567-8901-2345-6789-012345678901',
            'YOTI_KEY_FILE_PATH': '/home/user/.ssh/yoti_key.pem'
        }
    )

    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    failures = test_runner.run_tests(['django_yoti'])
    sys.exit(bool(failures))
