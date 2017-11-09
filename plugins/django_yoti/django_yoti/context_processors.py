from .settings import YOTI_APPLICATION_ID


def yoti_context(request=None):
    return application_context()


def application_context():
    return {'yoti_application_id': YOTI_APPLICATION_ID}
