import pytest

from ..login_button import get_login_button_html


def test_yoti_context(context):
    expected_keys = ('yoti_application_id', 'yoti_site_verification',
                     'yoti_login_button', 'yoti_login_button_sm',
                     'yoti_login_button_md', 'yoti_login_button_lg')
    assert set(context.keys()) == set(expected_keys)


def test_context_application_id(context, app_id):
    assert context.get('yoti_application_id') == app_id


def test_context_verification_key(context, verification_key):
    context_tag = context.get('yoti_site_verification')
    expected_html = '<meta name="yoti-site-verification" ' \
                    'content="{0}">'.format(verification_key)
    assert context_tag == expected_html


def test_context_predefined_login_buttons(context):
    assert 'data-size="small"' in context.get('yoti_login_button_sm')
    assert 'data-size="medium"' in context.get('yoti_login_button_md')
    assert 'data-size="large"' in context.get('yoti_login_button_lg')


def test_context_login_button_func(context, app_id, button_label):
    login_button_func = context.get('yoti_login_button')
    assert hasattr(login_button_func, '__call__')
    button_html = login_button_func(text=button_label, app_id=app_id)
    expected = '<span data-yoti-application-id="{0}" >' \
               '{1}</span>'.format(app_id, button_label)
    assert button_html == expected


@pytest.mark.parametrize('size', ('small', 'medium', 'large'))
def test_context_login_button_func_with_different_sizes(app_id, button_label, size):
    assert 'data-size="{0}"'.format(size) in get_login_button_html(
        size, button_label, app_id)
