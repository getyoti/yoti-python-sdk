def test_yoti_context(context):
    expected_key = 'yoti_application_id'
    assert expected_key in context.keys()


def test_context_application_id(context, app_id):
    assert context.get('yoti_application_id') == app_id
