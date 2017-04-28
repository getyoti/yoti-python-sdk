from django.test import TestCase, Client, RequestFactory
from django.http.response import HttpResponse, HttpResponseRedirectBase
from django.contrib.sessions.middleware import SessionMiddleware
from yoti_python_sdk.activity_details import ActivityDetails

from ..views import profile


class TestViews(TestCase):
    urls = 'django_yoti.urls'

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_auth_view(self):
        response = self.client.get('/auth/')
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        response = self.client.get('/login/')
        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)

    def test_profile_not_logged_in(self):
        request = self.factory.get('/profile')
        self._update_session(request)
        response = profile(request)
        self.assertIsInstance(response, HttpResponseRedirectBase)
        self.assertEqual(response.url, '/login/')

    def test_profile_outcome_is_failure(self):
        receipt = {'remember_me_id': 'some_id',
                   'sharing_outcome': 'FAILURE'}
        activity_details = ActivityDetails(receipt, None)

        request = self.factory.get('/profile/')
        self._update_session(request, activity_details=dict(activity_details))
        response = profile(request)

        self.assertIsInstance(response, HttpResponseRedirectBase)
        self.assertEqual(response.url, '/login/')

    def test_profile_outcome_is_success(self):
        user_id = 'some_id'
        user_profile = {'phone_number': '55555555'}
        receipt = {'remember_me_id': user_id,
                   'sharing_outcome': 'SUCCESS'}
        activity_details = ActivityDetails(receipt, None)
        activity_details.user_profile = user_profile

        request = self.factory.get('/profile/')
        self._update_session(request, activity_details=dict(activity_details))
        response = profile(request)

        self.assertIsInstance(response, HttpResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(getattr(request, 'yoti_user_id', None), user_id)
        self.assertEqual(getattr(request, 'yoti_user_profile', None), user_profile)

    @staticmethod
    def _update_session(request, **params):
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.update(params)
        request.session.save()
