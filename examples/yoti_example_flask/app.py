from flask import Flask, render_template, request

from yoti import Client

from settings import (
    YOTI_APPLICATION_ID,
    YOTI_CLIENT_SDK_ID,
    YOTI_FULL_KEY_FILE_PATH,
)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', app_id=YOTI_APPLICATION_ID)


@app.route('/auth')
def auth():
    client = Client(YOTI_CLIENT_SDK_ID, YOTI_FULL_KEY_FILE_PATH)
    activity_details = client.get_activity_details(request.args['token'])
    user_profile = activity_details.user_profile
    return render_template('profile.html',
                           **user_profile)


if __name__ == '__main__':
    app.run(debug=True)
