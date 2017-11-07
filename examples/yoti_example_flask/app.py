import os
from os.path import join, dirname
from binascii import a2b_base64
from dotenv import load_dotenv
from flask import Flask, render_template, request
from yoti_python_sdk import Client

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

from settings import (
    YOTI_APPLICATION_ID,
    YOTI_CLIENT_SDK_ID,
    YOTI_FULL_KEY_FILE_PATH,
)

app = Flask(__name__)

def save_image(base64_uri):
    base64_data_stripped = base64_uri[base64_uri.find(",")+1:]
    binary_data = a2b_base64(base64_data_stripped)
    upload_path = os.path.join(app.root_path, 'static', 'YotiSelfie.jpg')
    fd = open(upload_path, 'wb')
    fd.write(binary_data)
    fd.close()

@app.route('/')
def index():
    return render_template('index.html', app_id=YOTI_APPLICATION_ID)


@app.route('/yoti/auth')
def auth():
    client = Client(YOTI_CLIENT_SDK_ID, YOTI_FULL_KEY_FILE_PATH)
    activity_details = client.get_activity_details(request.args['token'])
    user_profile = activity_details.user_profile
    save_image(user_profile.get('selfie'))
    return render_template('profile.html',
                           **user_profile)

if __name__ == '__main__':
    app.run(debug=True)
