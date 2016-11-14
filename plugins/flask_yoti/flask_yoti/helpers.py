from flask.sessions import SecureCookieSession
from werkzeug.local import LocalProxy


def is_cookie_session(session):
    if isinstance(session, SecureCookieSession):
        return True
    if not isinstance(session, LocalProxy):
        return False
    if isinstance(session._get_current_object(), SecureCookieSession):
        return True
    return False
