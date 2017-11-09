import os

from flask import Response

from ..context_storage import activity_details_storage


def test_profile_view_not_logged_in(test_client):
    with test_client as _client:
        response = _client.get('/profile')
        assert isinstance(response, Response)
        assert getattr(response, 'status_code', None) == 302
        assert response.location.endswith('/login')


def test_profile_view_outcome_is_failure(test_client, activity_details_failure):
    with test_client as _client:
        activity_details_storage.save(activity_details_failure)
        with _client.session_transaction() as session:
            session['yoti_user_id'] = activity_details_failure.user_id
        response = _client.get('/profile')
        assert isinstance(response, Response)
        assert getattr(response, 'status_code', None) == 302
        assert response.location.endswith('/login')


def test_profile_view_outcome_is_success(test_client, app_id, activity_details_success):
    os.environ['YOTI_APPLICATION_ID'] = app_id
    with test_client as _client:
        activity_details_storage.save(activity_details_success)
        with _client.session_transaction() as session:
            session['yoti_user_id'] = activity_details_success.user_id
        response = _client.get('/profile')
        assert isinstance(response, Response)
        assert getattr(response, 'status_code', None) == 200
        assert 'Phone Number:' in str(response.data)
        assert '55555555' in str(response.data)
