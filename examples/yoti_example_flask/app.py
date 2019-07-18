# noinspection PyPackageRequirements
import os
from os.path import join, dirname

from dotenv import load_dotenv
from flask import Flask, render_template, request

from yoti_python_sdk import Client

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

from settings import (
    YOTI_SCENARIO_ID,
    YOTI_CLIENT_SDK_ID,
    YOTI_KEY_FILE_PATH,
)

app = Flask(__name__)


def save_image(selfie_data):
    upload_path = os.path.join(app.root_path, 'static', 'YotiSelfie.jpg')
    fd = open(upload_path, 'wb')
    fd.write(selfie_data)
    fd.close()


@app.route('/')
def index():
    return render_template('index.html', scenario_id=YOTI_SCENARIO_ID)


@app.route('/yoti/auth')
def auth():
    client = Client(YOTI_CLIENT_SDK_ID, YOTI_KEY_FILE_PATH)
    activity_details = client.get_activity_details(request.args['token'])
    profile = activity_details.profile
    profile_dict = vars(profile)

    context = profile_dict.get('attributes')
    context['base64_selfie_uri'] = getattr(activity_details, 'base64_selfie_uri')
    context['user_id'] = getattr(activity_details, 'user_id')
    context['parent_remember_me_id'] = getattr(activity_details, 'parent_remember_me_id')
    context['receipt_id'] = getattr(activity_details, 'receipt_id')
    context['timestamp'] = getattr(activity_details, 'timestamp')

    # change this string according to the age condition defined in dashboard
    age_verified = profile.get_attribute('age_over:18')
    if age_verified is not None:
        context['age_verified'] = age_verified

    selfie = context.get('selfie')
    if selfie is not None:
        save_image(selfie.value)
    return render_template('profile.html',
                           **context)


if __name__ == '__main__':
    app.run(host="0.0.0.0", ssl_context='adhoc')
