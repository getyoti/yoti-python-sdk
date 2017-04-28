import os

from flask import Flask, render_template, session
from flask_yoti import flask_yoti_blueprint
from flask_yoti.decorators import yoti_authenticated

YOTI_APPLICATION_ID = os.environ.get('YOTI_APPLICATION_ID')

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config.update(
    YOTI_APPLICATION_ID=YOTI_APPLICATION_ID,
    YOTI_CLIENT_SDK_ID=os.environ.get('YOTI_CLIENT_SDK_ID'),
    YOTI_KEY_FILE_PATH=os.environ.get('YOTI_KEY_FILE_PATH'),
    YOTI_LOGIN_VIEW='login',
    YOTI_REDIRECT_TO='profile'
)

app.register_blueprint(flask_yoti_blueprint, url_prefix='/yoti')


@app.route('/')
def index():
    return render_template('index.html', app_id=YOTI_APPLICATION_ID)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/profile')
@yoti_authenticated
def profile():
    user_profile = session.get('yoti_user_profile', {})
    return render_template('profile.html', **user_profile)


if __name__ == '__main__':
    app.run(debug=True)
