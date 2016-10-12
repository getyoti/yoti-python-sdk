from os import environ
from os.path import dirname, abspath, join, normpath
from flask import Flask, render_template, request

from yoti import YOTI_CLIENT_SDK_ID
from yoti.client import Client
app = Flask(__name__)


VERIFICATION_KEY = '81e15c45b1530282'

CURRENT_DIR = dirname(abspath(__file__))
DEFAULT_PEM_FILE = '../../yoti/tests/fixtures/sdk-test.pem'
PEM_FILE = environ.get('YOTI_SDK_PRIVATE_KEY', DEFAULT_PEM_FILE)
PEM_FILE_PATH = normpath(join(CURRENT_DIR, PEM_FILE))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/auth')
def auth():
    client = Client(YOTI_CLIENT_SDK_ID, PEM_FILE_PATH)
    activity_details = client.get_activity_details(request.args['token'])
    user_profile = activity_details.user_profile
    return render_template('profile.html', **user_profile)


@app.route('/auth/{0}'.format(VERIFICATION_KEY))
@app.route('/auth/{0}.html'.format(VERIFICATION_KEY))
def verify():
    return ''


if __name__ == '__main__':
    app.run(debug=True)
