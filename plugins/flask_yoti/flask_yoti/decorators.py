from functools import wraps
from flask import redirect, session, url_for

from .context_storage import activity_details_storage
from .settings import get_config_value
from .helpers import is_cookie_session


def yoti_authenticated(view_func):
    @wraps(view_func)
    def _decorated(*args, **kwargs):
        user_id = session.get('yoti_user_id')
        if not is_cookie_session(session):
            activity_details = session.get('activity_details')
        else:
            activity_details = activity_details_storage.get(user_id)
        if not activity_details or activity_details.outcome != 'SUCCESS':
            yoti_login_view = get_config_value('YOTI_LOGIN_VIEW')
            return redirect(url_for(yoti_login_view))

        session['yoti_user_id'] = activity_details.user_id
        session['yoti_user_profile'] = activity_details.user_profile

        return view_func(*args, **kwargs)

    return _decorated
