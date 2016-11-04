import os
import pytest

from flask import Flask
from flask_yoti import flask_yoti_blueprint
from flask_yoti.context_processors import yoti_context

from yoti.activity_details import ActivityDetails


@pytest.fixture(scope='module')
def test_client():
    app = Flask('test_app')
    app.secret_key = 'test app secret key'
    app.register_blueprint(flask_yoti_blueprint)
    return app.test_client()


@pytest.fixture(scope='module')
def activity_details_success():
    return _activity_details(outcome='SUCCESS')


@pytest.fixture(scope='module')
def activity_details_failure():
    return _activity_details(outcome='FAILURE')


def _activity_details(outcome='SUCCESS'):
    receipt = {
        'remember_me_id': 'some_user_id',
        'sharing_outcome': outcome
    }
    activity_details = ActivityDetails(receipt, None)
    activity_details.user_profile.update({
        'phone_number': '55555555'
    })
    return activity_details


@pytest.fixture
def context(app_id, verification_key):
    os.environ.update(
        YOTI_APPLICATION_ID=app_id,
        YOTI_VERIFICATION_KEY=verification_key,
    )
    return yoti_context()


@pytest.fixture(scope='module')
def app_id():
    return '01234567-8901-2345-6789-012345678901'


@pytest.fixture(scope='module')
def sdk_id():
    return '12345678-9012-3456-7890-123456789012'


@pytest.fixture(scope='module')
def verification_key():
    return '0123456789012345'


@pytest.fixture(scope='module')
def key_file_path():
    return '/home/user/.ssh/yoti_key.pem'


@pytest.fixture(scope='module')
def button_label():
    return 'Log in with Yoti'
