import os

from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
)

from yoti_python_sdk import Client
from .context_processors import yoti_context
from .context_storage import activity_details_storage
from .decorators import yoti_authenticated
from .helpers import is_cookie_session
from .settings import get_config_value

flask_yoti_blueprint = Blueprint('flask_yoti', __name__,
                                 template_folder='templates')
flask_yoti_blueprint.secret_key = os.urandom(24)
flask_yoti_blueprint.app_context_processor(yoti_context)


@flask_yoti_blueprint.route('/auth')
def auth():
    token = request.args.get('token')
    if not token:
        return render_template('yoti_auth.html')

    client_sdk_id = get_config_value('YOTI_CLIENT_SDK_ID')
    key_file_path = get_config_value('YOTI_KEY_FILE_PATH')
    client = Client(client_sdk_id, key_file_path)
    activity_details = client.get_activity_details(token)
    session['yoti_user_id'] = activity_details.user_id
    if not is_cookie_session(session):
        session['activity_details'] = dict(activity_details)
    else:
        activity_details_storage.save(activity_details)
    redirect_to = get_config_value('YOTI_REDIRECT_TO')
    return redirect(url_for(redirect_to))


@flask_yoti_blueprint.route('/login')
def login():
    return render_template('yoti_login.html')


@flask_yoti_blueprint.route('/profile')
@yoti_authenticated
def profile():
    user_profile = session.get('yoti_user_profile', {})
    return render_template('yoti_profile.html', **user_profile)
