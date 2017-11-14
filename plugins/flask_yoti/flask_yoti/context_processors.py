from .settings import get_config_value


def yoti_context():
    return application_context()


def application_context():
    yoti_application_id = get_config_value('YOTI_APPLICATION_ID')
    return {'yoti_application_id': yoti_application_id}
