from django.views.generic import TemplateView

from yoti import Client

from .app_settings import (
    YOTI_APPLICATION_ID,
    YOTI_CLIENT_SDK_ID,
    YOTI_FULL_KEY_FILE_PATH
)


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({'app_id': YOTI_APPLICATION_ID})


class AuthView(TemplateView):
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        client = Client(YOTI_CLIENT_SDK_ID, YOTI_FULL_KEY_FILE_PATH)
        activity_details = client.get_activity_details(request.GET['token'])
        context = activity_details.user_profile
        return self.render_to_response(context)
