from past.builtins import basestring

from yoti.activity_details import ActivityDetails


def live_test_requesting_activity_details_with_correct_data(
        client, encrypted_request_token):
    activity_details = client.get_activity_details(encrypted_request_token)

    assert isinstance(activity_details, ActivityDetails)
    assert activity_details.outcome == 'SUCCESS'
    selfie = activity_details.user_profile.get('selfie')
    assert isinstance(selfie, basestring)
    assert selfie.startswith('data:image/jpeg;base64')
